# payments/services/bank_statement_parser.py
"""
Bank Statement Parser - This is the most practical solution for Malawi banks.
You download CSV from internet banking, upload to Django, and it matches donations.
"""

import csv
import re
from datetime import datetime
from decimal import Decimal
from io import TextIOWrapper
from django.db import transaction

class BankStatementParser:
    """Parse bank statement CSV files and match with pending donations"""
    
    @staticmethod
    def parse_csv(csv_file):
        """
        Parse a bank statement CSV file
        
        How to use:
        1. Log into your bank's internet banking
        2. Go to Account Statement
        3. Select date range (e.g., last 7 days)
        4. Download as CSV/Excel
        5. Upload to Django admin
        """
        
        transactions = []
        
        # Read the uploaded file
        text_file = TextIOWrapper(csv_file, encoding='utf-8')
        reader = csv.reader(text_file)
        
        # Try to find the header row
        header = None
        rows = list(reader)
        
        for i, row in enumerate(rows):
            # Look for common header keywords
            row_text = ' '.join(row).lower()
            if 'date' in row_text and ('amount' in row_text or 'debit' in row_text):
                header = row
                data_rows = rows[i+1:]
                break
        
        if not header:
            # If no header found, assume first row is header
            header = rows[0]
            data_rows = rows[1:]
        
        # Find column indices
        col_indices = BankStatementParser._find_columns(header)
        
        # Parse each transaction
        for row in data_rows:
            if not row or len(row) < len(header):
                continue
                
            transaction = BankStatementParser._extract_transaction(row, col_indices)
            if transaction:
                transactions.append(transaction)
        
        return transactions
    
    @staticmethod
    def _find_columns(header):
        """Find which column contains what data"""
        indices = {
            'date': -1,
            'amount': -1,
            'reference': -1,
            'transaction_id': -1,
            'description': -1
        }
        
        for i, col in enumerate(header):
            col_lower = col.lower()
            
            if 'date' in col_lower:
                indices['date'] = i
            elif 'amount' in col_lower or 'debit' in col_lower or 'credit' in col_lower:
                indices['amount'] = i
            elif 'reference' in col_lower or 'ref' in col_lower:
                indices['reference'] = i
            elif 'transaction' in col_lower or 'id' in col_lower:
                indices['transaction_id'] = i
            elif 'description' in col_lower or 'narration' in col_lower or 'details' in col_lower:
                indices['description'] = i
        
        return indices
    
    @staticmethod
    def _extract_transaction(row, col_indices):
        """Extract transaction data from a CSV row"""
        
        # Extract date
        date = None
        if col_indices['date'] >= 0:
            date_str = row[col_indices['date']]
            date = BankStatementParser._parse_date(date_str)
        
        # Extract amount
        amount = None
        if col_indices['amount'] >= 0:
            amount_str = row[col_indices['amount']]
            amount = BankStatementParser._parse_amount(amount_str)
        
        if not amount:
            return None
        
        # Extract reference
        reference = ''
        if col_indices['reference'] >= 0:
            reference = row[col_indices['reference']]
        elif col_indices['description'] >= 0:
            reference = row[col_indices['description']]
        
        # Extract transaction ID
        transaction_id = ''
        if col_indices['transaction_id'] >= 0:
            transaction_id = row[col_indices['transaction_id']]
        
        return {
            'date': date or datetime.now(),
            'amount': float(amount),
            'reference': reference,
            'transaction_id': transaction_id,
            'raw_row': row
        }
    
    @staticmethod
    def _parse_date(date_str):
        """Parse date from various formats"""
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d',
            '%d %b %Y',
            '%d %B %Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except:
                continue
        return None
    
    @staticmethod
    def _parse_amount(amount_str):
        """Parse amount from string to Decimal"""
        try:
            # Remove currency symbols and commas
            cleaned = re.sub(r'[^0-9.-]', '', amount_str)
            return Decimal(cleaned)
        except:
            return None
    
    @staticmethod
    def match_with_donations(transactions, pending_donations):
        """Match bank transactions with pending donations"""
        
        matches = []
        
        for transaction in transactions:
            for donation in pending_donations:
                # Check if they match
                amount_matches = abs(transaction['amount'] - float(donation.amount)) < 0.01
                
                if not amount_matches:
                    continue
                
                # Check transaction ID match
                id_matches = (donation.transaction_id and 
                             donation.transaction_id == transaction['transaction_id'])
                
                # Check reference match
                reference_lower = transaction['reference'].lower()
                donor_in_ref = donation.donor_name.lower() in reference_lower
                notes_in_ref = donation.notes.lower() in reference_lower
                
                if amount_matches and (id_matches or donor_in_ref or notes_in_ref):
                    matches.append({
                        'donation': donation,
                        'transaction': transaction,
                        'confidence': 'high' if id_matches else 'medium'
                    })
                    break
        
        return matches
    
    @staticmethod
    def auto_verify_matches(matches, request=None):
        """Automatically verify matched donations"""
        
        verified_count = 0
        
        for match in matches:
            donation = match['donation']
            transaction = match['transaction']
            
            with transaction.atomic():
                donation.status = 'completed'
                donation.verified_by_api = True
                donation.verified_at = transaction['date']
                donation.verification_data = {
                    'matched_by': 'csv_import',
                    'confidence': match['confidence'],
                    'bank_reference': transaction['reference'],
                    'bank_date': transaction['date'].isoformat()
                }
                donation.save()
                verified_count += 1
        
        return verified_count
# payments/management/commands/import_bank_statement.py
"""
Django management command to import bank statements

How to use:
python manage.py import_bank_statement path/to/bank_statement.csv
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from payments.models import Donation
from payments.services.bank_statement_parser import BankStatementParser

class Command(BaseCommand):
    help = 'Import bank statement CSV and match with pending donations'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--dry-run', action='store_true', help='Preview matches without saving')
    
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS(f'\n📁 Reading bank statement: {csv_file_path}\n'))
        
        # Read and parse the CSV file
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                transactions = BankStatementParser.parse_csv(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error reading file: {str(e)}'))
            return
        
        self.stdout.write(f'📊 Found {len(transactions)} transactions in bank statement\n')
        
        # Get pending bank donations
        pending_donations = Donation.objects.filter(
            payment_method='bank',
            status='pending'
        )
        
        self.stdout.write(f'💰 Found {pending_donations.count()} pending donations\n')
        
        if pending_donations.count() == 0:
            self.stdout.write(self.style.WARNING('No pending donations to match.'))
            return
        
        # Match transactions with donations
        matches = BankStatementParser.match_with_donations(transactions, pending_donations)
        
        self.stdout.write(f'🎯 Found {len(matches)} matches!\n')
        
        if len(matches) == 0:
            self.stdout.write(self.style.WARNING('No matches found. Check your CSV format.'))
            return
        
        # Display matches
        for i, match in enumerate(matches, 1):
            donation = match['donation']
            transaction = match['transaction']
            
            self.stdout.write(f'\n📌 Match #{i}:')
            self.stdout.write(f'   Donor: {donation.donor_name}')
            self.stdout.write(f'   Amount: MWK {donation.amount}')
            self.stdout.write(f'   Transaction ID: {donation.transaction_id or "Not provided"}')
            self.stdout.write(f'   Bank Reference: {transaction["reference"][:50]}')
            self.stdout.write(f'   Bank Date: {transaction["date"].strftime("%Y-%m-%d")}')
            self.stdout.write(f'   Confidence: {match["confidence"].upper()}')
        
        # Confirm and save
        if not dry_run:
            self.stdout.write('\n' + '='*50)
            confirm = input('✅ Do you want to verify these donations? (yes/no): ')
            
            if confirm.lower() == 'yes':
                verified = BankStatementParser.auto_verify_matches(matches)
                self.stdout.write(self.style.SUCCESS(f'\n✨ Successfully verified {verified} donations!'))
                
                # Send confirmation emails
                for match in matches:
                    donation = match['donation']
                    if donation.donor_email:
                        self.stdout.write(f'   📧 Email sent to {donation.donor_email}')
            else:
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠️ DRY RUN - No changes were made'))
            self.stdout.write('   Run without --dry-run to verify donations')
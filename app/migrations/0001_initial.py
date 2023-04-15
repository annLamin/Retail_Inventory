# Generated by Django 3.1.5 on 2021-10-08 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('hide_email', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('telephone', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Depositor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('telephone', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciepient', models.CharField(max_length=60)),
                ('desc', models.TextField()),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('acc', 'Accessories'), ('mob', 'Mobile'), ('ele', 'Electronics')], max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('brand', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('desc', models.TextField()),
                ('total_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('acc', 'Accessories'), ('mob', 'Mobile'), ('ele', 'Electronic')], max_length=30)),
                ('telephone', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('telephone', models.IntegerField()),
                ('salary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Withdraw', 'Withdraw'), ('Deposit', 'Deposit')], max_length=45)),
                ('amount', models.IntegerField()),
                ('description', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('depositor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.depositor')),
            ],
        ),
        migrations.CreateModel(
            name='Sup_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('telephone', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('actual_total_price', models.IntegerField(default=0)),
                ('total_amount_paid', models.IntegerField()),
                ('cust_name', models.CharField(max_length=30)),
                ('cust_tel', models.IntegerField()),
                ('cust_address', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Salaries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.CharField(max_length=30)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sale')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('desc', models.CharField(default='N/A', max_length=100)),
                ('total_amount', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sale')),
            ],
        ),
        migrations.CreateModel(
            name='Cashier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('telephone', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Borrower_Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Payment', 'Payment'), ('Borrow', 'Borrow')], max_length=45)),
                ('amount', models.IntegerField()),
                ('description', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.borrower')),
            ],
        ),
    ]
# MOBI - Mobile Banking Application

MOBI is a robust Django-based mobile banking application that provides secure and efficient banking services through a RESTful API. This application enables users to perform various banking operations including money transfers, account management, and transaction tracking.

## 🌟 Features

### Core Banking Features
- **Account Management**
  - Create and manage user accounts
  - Secure PIN authentication
  - Balance tracking
  - Account statements

### Transaction Capabilities
- **Money Transfers**
  - User-to-user transfers
  - Real-time balance updates
  - Transaction history
  - Reference number generation

### Security
- PIN verification for transactions
- Secure password hashing
- Transaction atomicity
- Protected API endpoints

### API Features
- RESTful API architecture
- Token-based authentication
- Comprehensive API documentation
- Rate limiting

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/steve-ongera/mobi.git
cd mobi
```

2. **Create and activate virtual environment**
```bash
# For Unix/macOS
python -m venv env
source env/bin/activate

# For Windows
python -m venv env
.\env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file**
Create a `.env` file in the root directory with the following content:
```env
DB_NAME=mobi_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DJANGO_SECRET_KEY=your-secret-key-here
```

5. **Create MySQL database**
```sql
CREATE DATABASE mobi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Run the development server**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📚 API Documentation

### Authentication Endpoints

#### Create Account
```http
POST /api/users/
Content-Type: application/json

{
    "username": "string",
    "password": "string",
    "phone_number": "string",
    "pin": "string"
}
```

#### Perform Transfer
```http
POST /api/users/{id}/transfer/
Content-Type: application/json

{
    "receiver_account": "string",
    "amount": "number",
    "pin": "string"
}
```

### Response Examples

#### Successful Transfer
```json
{
    "message": "Transfer successful"
}
```

#### Error Response
```json
{
    "error": "Insufficient funds"
}
```

## 🔧 Configuration

### Database Configuration
The application uses MySQL as its database. Configure your database settings in `settings.py` or through environment variables:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'mobi_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| DB_NAME | Database name | mobi_db |
| DB_USER | Database username | root |
| DB_PASSWORD | Database password | - |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 3306 |
| DJANGO_SECRET_KEY | Django secret key | - |

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

For coverage report:
```bash
coverage run manage.py test
coverage report
```

## 🔐 Security Considerations

1. **PIN Security**
   - PINs are stored using secure hashing
   - Rate limiting on PIN attempts
   - Temporary account lockout after multiple failed attempts

2. **Transaction Security**
   - All transactions are atomic
   - Validation checks before any transfer
   - Transaction logging for audit trails

3. **API Security**
   - Token-based authentication
   - CORS configuration
   - Request rate limiting

## 🛠 Development

### Code Style
This project follows PEP 8 guidelines. Use flake8 for linting:
```bash
flake8 .
```

### Making Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## 👥 Contributors

- [SteveOngera] - Initial work - [steve-ongera]

## 🙏 Acknowledgments

- Django documentation
- Django REST framework
- MySQL community

## 📞 Support

For support, email support@mobiapp.com or create an issue in the GitHub repository.

## 🚀 Future Enhancements

- Mobile money integration
- Bill payments
- Scheduled transfers
- Push notifications
- Account statements export (PDF/CSV)
- Multi-currency support

---

Made with ❤️ by Steveongera | InnovationHub Ltd
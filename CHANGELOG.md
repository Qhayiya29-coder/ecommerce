# Changelog

All notable changes and improvements to this project.

## [1.0.0] - 2024-12-06

### Added
- Complete Django eCommerce application with vendor and buyer functionality
- Authentication system with registration, login, logout
- Password reset functionality with email integration
- Vendor store and product management
- Buyer shopping cart and checkout system
- Product review system with verified purchase badges
- Order history and order detail views for buyers
- Session-based cart persistence
- Email integration for invoices and password resets
- Admin panel configuration for all models
- Management command for setting up groups and permissions
- Comprehensive documentation (README, SETUP_GUIDE, CONTRIBUTING)
- .gitignore file for proper version control
- LICENSE file (MIT License)
- Startup scripts (start_server.bat, start_server.ps1)

### Improved
- Added error handling for invalid quantity in add_to_cart view
- Added POST method validation for add_to_cart
- Enhanced order management with order history feature
- Improved navigation with "My Orders" link for buyers
- Better error messages and user feedback

### Security
- CSRF protection on all forms
- Password strength validation
- Token-based password reset with expiry
- Permission checks on all sensitive views
- Secure password hashing (Django default)

### Fixed
- URL namespace issue (removed duplicate URL includes)
- Static files directory warning
- Template group checks to handle users without groups

### Documentation
- Complete README with installation instructions
- Quick setup guide
- Contributing guidelines
- Troubleshooting section


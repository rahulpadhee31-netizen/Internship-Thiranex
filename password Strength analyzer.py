import string

password = input("Enter your password: ")

score = 0

# Check length
if len(password) >= 8:
    score += 1

if len(password) >= 12:
    score += 1

# Check lowercase
if any(c.islower() for c in password):
    score += 1

# Check uppercase
if any(c.isupper() for c in password):
    score += 1

# Check digit
if any(c.isdigit() for c in password):
    score += 1

# Check special character
if any(c in string.punctuation for c in password):
    score += 1

print("\nPassword Strength:")

if score <= 2:
    print("Weak")
elif score <= 4:
    print("Moderate")
elif score <= 5:
    print("Strong")
else:
    print("Very Strong")

print("\nSuggestions:")

if len(password) < 12:
    print("- Use at least 12 characters")

if not any(c.isupper() for c in password):
    print("- Add uppercase letters")

if not any(c.islower() for c in password):
    print("- Add lowercase letters")

if not any(c.isdigit() for c in password):
    print("- Add numbers")

if not any(c in string.punctuation for c in password):
    print("- Add special characters")

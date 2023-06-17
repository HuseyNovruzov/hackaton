import re
import passlib.pwd

# Email verifier regex
def isValidEmail(email):
    email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.fullmatch(email_regex, email):
      return True
    else:
      False

def isValidPhoneNumber(phone):
   phone_regex = re.compile(r"^(70|77|50|10|55|99)\d{7}$")
   if re.fullmatch(phone_regex, phone):
      return True
   return False

def isValidPassword(password):
    # define our regex pattern for validation
    pattern = r""
    print(password)

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)


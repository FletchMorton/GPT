# Just a little tour of py features I suppose

username = input("Username: ")

while len(username) <= 0 | username.isalpha() == False:
    print("\nUsername must have at least 1 character and only contain alphabetical characters!\n")
    username = input("\nRe-Enter Username: ")

password = input("Password: ")

if username.isalpha() == False:
    print("\nUsername must only contain alphabetical characters!\n")
elif username == "Luffy":
    print("\nUsername accepted!\n")
else:
    print("\nUsername not found in the system!\n")




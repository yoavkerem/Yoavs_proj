s1 = "איש שלג"
s2 = "שקיעה"
sall = f"{s1} {s2}"
print(f"len(sall) = {len(sall)}")
encoded_sall = sall.encode("utf-8")

print(f"len(encoded_sall = {len(encoded_sall)}")
zfill_length = str(len(encoded_sall)).zfill(2)
print(zfill_length)
print()
print(f"encoded_sall = {encoded_sall}")
decoded_sall = encoded_sall.decode()
print(f"len(decoded_sall = {len(decoded_sall)}")
print(f"decoded_sall = {decoded_sall}")
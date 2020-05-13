from faker import Faker
import csv

fake = Faker()
print(fake.simple_profile())
field_names = ['customer_id', 'username', 'name', 'sex', 'mail', 'birthdate']

with open('/home/kit/polynote/customer_ids_hbase.txt', 'w') as fout:
    csv_out = csv.DictWriter(fout, field_names, extrasaction='ignore', delimiter='\t')
    with open('/home/kit/polynote/customer_ids.txt', 'r') as cust_file:
        for line in cust_file:
            p = fake.simple_profile()
            p['customer_id'] = line.strip()
            csv_out.writerow(p)

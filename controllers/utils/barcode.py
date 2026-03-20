import barcode
import random
from barcode.writer import ImageWriter
from controllers.utils import Utils
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
class Barcode:
    def __init__(self, dbms=None, object=None) -> None:
        self.dbms = dbms
        self.object = object
        
    @classmethod
    def generate_random_ean13_digits(cls):
        digits = [str(random.randint(0, 9)) for _ in range(12)]
        check_digit = cls.__calculate_ean13_check_digit(cls, digits)
        digits.append(check_digit)
        barcode = ''.join(digits)
        return barcode

    def __calculate_ean13_check_digit(self, digits):
        odd_sum = sum(int(digit) for i, digit in enumerate(digits) if i % 2 == 0)
        even_sum = sum(int(digit) for i, digit in enumerate(digits) if i % 2 == 1)
        check_digit = (10 - ((odd_sum + even_sum * 3) % 10)) % 10
        return str(check_digit)
    
    def generate_ean_13(self, code):
        try:
            ean = barcode.EAN13(code, writer=ImageWriter())
            base_path = utils.get_path_to_base_folder()
            file = f"/media/{self.dbms.host}/private/{code}"
            filepath = f"{base_path}{file}"
            ean.save(filepath)
            return utils.respond(utils.ok, f"{file}.png")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{e}")     

    def generate_code128(self, code):
        try:
            barcode_class = barcode.get_barcode_class('code128')
            code128 = barcode_class(code, writer=ImageWriter())
            base_path = utils.get_path_to_base_folder()

            # Save the barcode as an image
            file = f"/media/{self.dbms.host}/private/{code}"
            filepath = f"{base_path}{file}"
            code128.save(filepath)

            return utils.respond(utils.ok, f"{file}.png")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{e}")   
            
    def check_if_barcode_exits(self, code, model, field_name):
        fetch_model = self.dbms.get_doc(model, str(code), fetch_by_field=field_name, privilege=True)
        if fetch_model.status == utils.ok:
            return True
        else:
            return False




class AuthenticateBase:
        
    def _validation_fail(self, error_text, bool_type, button_bool_value, entry_style, entry_style_value, function):
        if (bool_type == "email"):
            self.c_email = button_bool_value
        elif (bool_type == "password"):
            self.c_password = button_bool_value
        elif (bool_type == "username"):
            self.c_username = button_bool_value
        elif (bool_type == "otp"):
            self.c_otp = button_bool_value
        self.errors.set(error_text)
        entry_style["style"] = entry_style_value
        function()
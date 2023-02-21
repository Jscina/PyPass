from flask import Blueprint

kwargs = {
    "name":"recover_account_view",
    "import_name":__name__,
    "url_prefix":"/"
}

recover_account_view = Blueprint(**kwargs)

# Recover Account section
@recover_account_view.route('/recover_account', methods=['GET'])
def recover_account():
    return None

from utils.response import fail


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return fail("Resource tidak ditemukan"), 404

    @app.errorhandler(Exception)
    def internal_error(error):
        return fail(str(error)), 500

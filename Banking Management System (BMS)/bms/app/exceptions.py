class AppError(Exception):
    status_code = 400
    name = "app_error"

    def __init__(self, message: str = "", status_code: int = None):
        super().__init__(message)
        self.message = message
        if status_code:
            self.status_code = status_code


class NotFoundError(AppError):
    name = "not_found"
    status_code = 404


class ValidationError(AppError):
    name = "validation_error"
    status_code = 422

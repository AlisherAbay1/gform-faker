class BaseGformFakerError(Exception):
    pass

class TorNotConnectedError(BaseGformFakerError):
    pass

class UnableToGetFbzxError(BaseGformFakerError):
    pass

class UnableToParseFbzxError(BaseGformFakerError):
    pass

class UnableToParseFbPublicLoadDataError(BaseGformFakerError):
    pass

class UndefinedQuestionTypeError(BaseGformFakerError):
    pass
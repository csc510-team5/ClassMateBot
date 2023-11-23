import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
from pprint import pprint


configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = 'CA71FA0C-475C-451E-B35C-7E0B157CC00F'

# create an instance of the API class
api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))

try:
    api_request = ProWritingAidSDK.TextAnalysisRequest('''zed Frodo became aware that there was a great stir and
movement on the plain. It seemed as if whole armies were on the
march, though for the most part they were hidden by the reeks and
fumes drifting from the fens and wastes beyond. But here and there
he caught the gleam of spears and helmets; and over the levels beside
the roads horsemen could be seen riding in many companies. He
remembered his vision from afar upon Amon Hen, so few days before,
though now it seemed many years ago. Then he knew that the hope
that had for one wild moment stirred in his heart was vain. The
trumpets had not rung in ch''',
                                                       ["plagiarism"],
                                                       "General",
                                                       "en")
    api_response = api_instance.post(api_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling API: %s\n" % e)
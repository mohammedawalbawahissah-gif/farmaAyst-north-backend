import uuid
import requests
from django.conf import settings


class MoMoService:
    """MTN Mobile Money API integration."""

    BASE_URL = settings.MOMO_BASE_URL
    SUBSCRIPTION_KEY = settings.MOMO_SUBSCRIPTION_KEY

    def _headers(self, reference_id=None):
        return {
            'X-Reference-Id': reference_id or str(uuid.uuid4()),
            'X-Target-Environment': settings.MOMO_ENVIRONMENT,
            'Ocp-Apim-Subscription-Key': self.SUBSCRIPTION_KEY,
            'Content-Type': 'application/json',
        }

    def request_to_pay(self, amount: str, phone: str, reference: str, narration: str) -> dict:
        """Initiate a MoMo collection (repayment from farmer)."""
        ref_id = str(uuid.uuid4())
        payload = {
            'amount': amount,
            'currency': 'GHS',
            'externalId': reference,
            'payer': {'partyIdType': 'MSISDN', 'partyId': phone},
            'payerMessage': narration,
            'payeeNote': narration,
        }
        try:
            resp = requests.post(
                f'{self.BASE_URL}/collection/v1_0/requesttopay',
                json=payload,
                headers=self._headers(ref_id),
                timeout=30,
            )
            return {'success': resp.status_code == 202, 'reference_id': ref_id,
                    'status_code': resp.status_code, 'response': resp.text}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}

    def transfer(self, amount: str, phone: str, reference: str, narration: str) -> dict:
        """Initiate a MoMo disbursement (payout to farmer)."""
        ref_id = str(uuid.uuid4())
        payload = {
            'amount': amount,
            'currency': 'GHS',
            'externalId': reference,
            'payee': {'partyIdType': 'MSISDN', 'partyId': phone},
            'payerMessage': narration,
            'payeeNote': narration,
        }
        try:
            resp = requests.post(
                f'{self.BASE_URL}/disbursement/v1_0/transfer',
                json=payload,
                headers=self._headers(ref_id),
                timeout=30,
            )
            return {'success': resp.status_code == 202, 'reference_id': ref_id,
                    'status_code': resp.status_code}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}

    def check_status(self, reference_id: str, operation: str = 'collection') -> dict:
        endpoint = 'collection' if operation == 'collection' else 'disbursement'
        try:
            resp = requests.get(
                f'{self.BASE_URL}/{endpoint}/v1_0/requesttopay/{reference_id}',
                headers=self._headers(),
                timeout=30,
            )
            return {'success': True, 'data': resp.json()}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}


class PaystackService:
    """Paystack payment integration for card/bank transfers."""

    BASE_URL = 'https://api.paystack.co'

    def _headers(self):
        return {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

    def initialize_transaction(self, email: str, amount_ghs: float, reference: str, callback_url: str = '') -> dict:
        payload = {
            'email': email,
            'amount': int(amount_ghs * 100),  # Paystack uses pesewas
            'reference': reference,
            'currency': 'GHS',
            'callback_url': callback_url,
        }
        try:
            resp = requests.post(f'{self.BASE_URL}/transaction/initialize',
                                 json=payload, headers=self._headers(), timeout=30)
            data = resp.json()
            return {'success': data.get('status'), 'data': data.get('data', {})}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}

    def verify_transaction(self, reference: str) -> dict:
        try:
            resp = requests.get(f'{self.BASE_URL}/transaction/verify/{reference}',
                                headers=self._headers(), timeout=30)
            data = resp.json()
            return {'success': data.get('status'), 'data': data.get('data', {})}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}


class HubtelSMSService:
    """Hubtel SMS for Ghana-local notifications."""

    BASE_URL = 'https://smsc.hubtel.com/v1/messages/send'

    def send(self, to: str, message: str) -> dict:
        try:
            resp = requests.get(self.BASE_URL, params={
                'clientsecret': settings.HUBTEL_CLIENT_SECRET,
                'clientid': settings.HUBTEL_CLIENT_ID,
                'from': settings.HUBTEL_SENDER_ID,
                'to': to,
                'content': message,
            }, timeout=20)
            return {'success': resp.status_code == 200, 'response': resp.text}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}


momo_service    = MoMoService()
paystack_service = PaystackService()
sms_service     = HubtelSMSService()

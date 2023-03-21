from web3 import Web3
import json
from pprint import pprint

# 이더리움 노드 연결 (여기서는 Infura를 사용)
infura_url = "https://mainnet.infura.io/v3/358b82d672c740a1b26c3e5854ecdcc2"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Uniswap V2 계약 주소 및 ABI
uniswap_v2_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
with open("UniswapV2Factory.json", "r") as f:
    uniswap_v2_factory_json = json.load(f)
    uniswap_v2_abi = uniswap_v2_factory_json["abi"]
# Uniswap V2 스마트 계약 객체 생성
uniswap_v2_contract = w3.eth.contract(address=w3.to_checksum_address(uniswap_v2_address), abi=uniswap_v2_abi)

# 관심 있는 블록 번호 범위
start_block = 16870000
end_block = 16874326

# 'PairCreated' 이벤트 시그니처 가져오기
pair_created_event_signature = w3.keccak(text="PairCreated(address,address,address,uint256)").hex()

# 필터 설정 및 이벤트 로그 가져오기
event_filter = w3.eth.filter({"fromBlock": start_block, "toBlock": end_block, "address": uniswap_v2_address, "topics": [pair_created_event_signature]})
event_logs = event_filter.get_all_entries()

# 이벤트 로그 출력
for event_log in event_logs:
    event_data = uniswap_v2_contract.events.PairCreated().process_log(event_log)
    print(event_data)

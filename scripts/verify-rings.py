from pathlib import Path
import re
import sys

expected = {
    'DP_RXDMA_BUF_RING_SIZE': 2048,
    'DP_RXDMA_REFILL_RING_SIZE': 2048,
    'DP_RXDMA_MON_STATUS_RING_SIZE': 512,
    'DP_RXDMA_MONITOR_BUF_RING_SIZE': 2048,
    'DP_RXDMA_MONITOR_DST_RING_SIZE': 1024,
    'DP_RXDMA_MONITOR_DESC_RING_SIZE': 2048,
}
paths = [p for p in Path(sys.argv[1]).rglob('dp.h')
         if p.as_posix().endswith('/drivers/net/wireless/ath/ath11k/dp.h')
         and 'backports-6.18.26' in p.as_posix()]
assert paths, 'Prepared ath11k source not found'
for path in paths:
    text = path.read_text()
    for name, value in expected.items():
        match = re.search(r'^#define\s+' + name + r'\s+(\d+)\s*$', text, re.M)
        assert match and int(match[1]) == value, f'{path}: unexpected {name}'
    print(f'PASS: {path}; five rings reduced, refill buffer remains 2048')

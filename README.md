# MX4200 v1: experimental ath11k RAM mitigation

This recipe builds OpenWrt v25.12.5 for **Linksys MX4200 v1 only**,
using the release commit and release-pinned package feeds.
It applies a community mitigation that halves five ath11k RX/monitor
ring constants. `DP_RXDMA_REFILL_RING_SIZE` remains **2048** because
that constant describes the receive buffer size, not ring depth.

Sources:
- https://github.com/openwrt/openwrt/issues/24154
- https://github.com/openwrt/openwrt/pull/25166
- https://github.com/enspect/ath11k-ipq807x-rx-buffer-oom-fix

The patch derives from the GPL-2.0 community patch. It is not an
upstream-approved fix, and has not yet been runtime-tested on the target
router for this build. Driver buffering and peak performance may change.
Successful compilation does not establish safety or solve every OOM cause.

## Build

Use Actions → Build MX4200 v1 experimental ath11k fix → Run workflow.
Only a manual dispatch runs the build. No router configuration or secrets
are included. The workflow never connects to or flashes a router.

Artifacts include the sysupgrade image, SHA256, package manifest, build
configuration, source pinning, the patch, and driver module build hashes.
The mac80211 package release is bumped to distinguish patched packages.

## Deployment gates

Before flashing TB2:
1. Download and check the firmware SHA256.
2. Verify the embedded image profile is `linksys,mx4200v1`.
3. Save TB2's configuration backup off-router and export its package list.
4. Have local wired management and a recovery route available; mesh will
   disconnect during upgrade and may not recover if the driver fails.
5. Run the router's `sysupgrade -T` validation on the image. Do not force
   an image that fails validation.
6. Compare the artifact package manifest to the installed package list;
   this recipe includes full wpad-mbedtls, LuCI and basic diagnostics, but
   is not a complete reproduction of every installed user package.
7. Keep the existing manual mesh configuration and mesh11sd disabled.

Do not mix kernel modules from this custom build with official firmware
or force-install mismatched official kernel modules into this image.
Keep the patched artifact and a compatible stock rollback image.

Test TB2 before TB1. Monitor RAM, mesh peer connectivity, Wi-Fi clients,
DNS, Internet and throughput under comparable traffic for at least 24 h.

Patch file: GPL-2.0-only, matching the ath11k source and original mitigation.
Local build/verification scripts and recipe: MIT.

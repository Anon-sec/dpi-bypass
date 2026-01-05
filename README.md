# dpi-bypass

This is a small application-level proxy meant for situations where websites are blocked using DPI-based methods.

It runs locally and only affects applications that are configured to use it.  
For example, a browser can be configured to use the proxy by pointing it to the loopback address shown in the terminal or command prompt after running `main.py`.

This is **not a VPN**.

---

## Alternatives

If you want a **more efficient or system-wide DPI bypass**, there are better tools available.

GoodbyeDPI is a popular Windows tool that works at the system level and is usually more effective when you want all traffic to be affected without configuring individual applications:

https://github.com/ValdikSS/GoodbyeDPI

Another good project is PowerTunnel, which also focuses on DPI bypass and was used as inspiration while exploring this space:

https://github.com/krlvm/PowerTunnel

If those tools fit your needs, you should use them instead of this project.

---

## What this project is

This project does something similar in spirit, but at a different level.

Instead of working inside the operating system, it works at the **application level**.  
Applications that use this proxy send their traffic through it, and applications that do not are unaffected.

If you configure system proxy settings to send traffic through the loopback address, more applications may use it, depending on how they respect system proxy settings.

It is meant to be simple, visible, and easy to reason about.

---

## What you should know before using it

You do not need deep networking knowledge.

It helps to understand:
- what DPI is
- why some networks use DPI-based blocking
- whether a site is blocked because of DPI or for some other reason

For background context, just searching these terms online is enough:
- DPI
- encrypted DNS (DoH)
- TLS handshake
- what is HTTPS

You do not need to fully understand these topics to use the tool.

---

## When this makes sense to use

Use this when:
- a site is blocked on your network
- the block seems DPI-related
- the site works on other networks
- you only want certain applications or browsers to be affected

---

## When you should use a VPN instead

This tool will not help if:
- the site blocks your IP address
- the site blocks your country or region
- the site itself refuses connections from your network
- you want stronger privacy or security

In those cases, a VPN is the correct solution.

---

## About QUIC

Some browsers and applications use QUIC, which is a UDP-based protocol instead of HTTPS over TCP.  
This proxy does not handle QUIC traffic, so connections using QUIC will bypass it.

If you want this proxy to affect browser traffic, you may need to disable QUIC in the browser so it falls back to standard HTTPS.  
Whether you should disable QUIC depends on your use case. Disabling it is usually fine for testing or bypass scenarios, but it is not required for normal browsing.

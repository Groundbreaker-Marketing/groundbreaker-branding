import sys, os
T = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/"
sys.path.insert(0, T + "tools")
sys.argv = ["prep_close.py"] + [T + n + ".json" for n in ("vsl", "web-highlight", "web-google-leads", "web-more-work", "web-coaching", "employee-insert")]
import prep_close
prep_close.main()

site_code = "g2b"
typeof    = "list"

if site_code == "g2b" : 
    import application.g2b as g2b
    ca = g2b.realize(typeof)
    ca.run()
elif site_code == "kepco":
    import application.kepco as kepco
    ca = kepco.realize(typeof)
    ca.run()

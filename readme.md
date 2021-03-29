## This is adobe premiere pro script for LJMedia.

auto injection Tensorflow output in adobe premiere pro.

![image](my_memory_doc/demo.gif)

## How this work

![image](my_memory_doc/flow_doc.jpg)


## compiler

### create signed key

```bash
bin/ZXPSignCmd.exe -selfSignedCert <countryCode> <stateOrProvince> <organization> <commonName> <password> <outputPath.p12> [options]
```

### build

```bash
bin/ZXPSignCmd.exe -sign "../extensionSource" myExt.zxp myCert.p12 myPassword123
```

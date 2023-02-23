qr_decomp_and_qury_matching.py takes the input gathered from 3.5.1 and creates a query q 
based on "philosophical sounding" sentences. It then queries the matrix W to produce a matching 
author, and then queries W_QRD, the matrix obtained by getting a QR decomposition
and reducing the rank of R and multiplying by Q. 

This was a success! The last sentence is taken straight from an Oscar Wilde book, and matches to
Oscar Wilde. The two queries have matched every single time, so the rank reduction worked!



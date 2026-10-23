# Nhan 2 da thuc trong truong huu han GF(2^m)
# Da thuc bieu dien bang so nguyen: moi bit la 1 he so
# vd: x^3 + x + 1 = 0b1011 = 11

# da thuc toi gian
P4 = 0b10011        # x^4 + x + 1
P8 = 0b100011011    # x^8 + x^4 + x^3 + x + 1 (cai cua AES)


def bac(a):
    # bac cua da thuc = vi tri bit 1 cao nhat
    d = -1
    while a > 0:
        a >>= 1
        d += 1
    return d


def nhan_thuong(a, b):
    # nhan 2 da thuc tren GF(2), chua rut gon
    # cong = XOR
    kq = 0
    while b > 0:
        if b & 1:
            kq ^= a
        a <<= 1
        b >>= 1
    return kq


def chia_du(a, p):
    # lay a mod p
    dp = bac(p)
    while bac(a) >= dp:
        a ^= p << (bac(a) - dp)
    return a


def nhan_gf(a, b, p):
    # cach 1: nhan thuong roi chia du cho da thuc toi gian
    return chia_du(nhan_thuong(a, b), p)


def nhan_gf2(a, b, p):
    # cach 2: vua nhan vua rut gon (russian peasant)
    m = bac(p)
    kq = 0
    while b > 0:
        if b & 1:
            kq ^= a
        b >>= 1
        a <<= 1
        if (a >> m) & 1:   # tran bac thi tru di p
            a ^= p
    return kq


def in_da_thuc(a):
    if a == 0:
        return "0"
    ds = []
    for i in range(bac(a), -1, -1):
        if (a >> i) & 1:
            if i == 0:
                ds.append("1")
            elif i == 1:
                ds.append("x")
            else:
                ds.append("x^%d" % i)
    return " + ".join(ds)


if __name__ == "__main__":
    print("=== GF(2^4), p(x) = x^4 + x + 1 ===")
    for a, b in [(0b0111, 0b1001), (0b1010, 0b0110), (0b1111, 0b1111)]:
        c = nhan_gf(a, b, P4)
        print("(%s) * (%s) = %s" % (in_da_thuc(a), in_da_thuc(b), in_da_thuc(c)))

    print()
    print("=== GF(2^8), p(x) = x^8 + x^4 + x^3 + x + 1 ===")
    for a, b in [(0x57, 0x83), (0x02, 0x80), (0xFF, 0xFF)]:
        c = nhan_gf(a, b, P8)
        print("0x%02X * 0x%02X = 0x%02X" % (a, b, c))

    # kiem tra 2 cach ra giong nhau
    ok = True
    for a in range(16):
        for b in range(16):
            if nhan_gf(a, b, P4) != nhan_gf2(a, b, P4):
                ok = False
    for a in range(256):
        for b in range(256):
            if nhan_gf(a, b, P8) != nhan_gf2(a, b, P8):
                ok = False
    print()
    print("2 cach khop nhau:", ok)
import hashlib
import secrets


# ==============
# Yardımcı fonksiyonlar
# ==============

def hash_to_int(x: str, p: int) -> int:
    """
    String x'i SHA-256 ile hashleyip mod p alır.
    """
    h = hashlib.sha256(x.encode()).hexdigest()
    return int(h, 16) % p


def generate_random_sets(total_size: int, overlap_size: int):
    """
    total_size: Her bir setin toplam eleman sayısı (|A| ve |B|)
    overlap_size: Kesişimde olmasını istediğimiz eleman sayısı (|A ∩ B|)

    Çıktı: (set_A, set_B)
    """
    assert overlap_size <= total_size, "Overlap total_size'dan büyük olamaz."

    # Ortak elemanlar
    common = {
        f"common_{i}_{secrets.token_hex(4)}"
        for i in range(overlap_size)
    }

    # A'ya özel elemanlar
    unique_A = {
        f"A_{i}_{secrets.token_hex(4)}"
        for i in range(total_size - overlap_size)
    }

    # B'ye özel elemanlar
    unique_B = {
        f"B_{i}_{secrets.token_hex(4)}"
        for i in range(total_size - overlap_size)
    }

    set_A = common.union(unique_A)
    set_B = common.union(unique_B)

    return set_A, set_B


# ==============
# DH-PSI protokol adımları
# ==============

def dh_psi(set_A, set_B):
    """
    İki tarafın setlerini alır, DH tabanlı PSI yapar.
    Çıktı: (real_intersection, computed_intersection)
    """

    # 1) Ortak grup parametreleri
    p = 2**127 - 1  # öğretimsel amaçlı büyük asal
    g = 5

    # 2) Alice ve Bob gizli üslerini seçsin
    a = secrets.randbelow(p - 2) + 1  # 1..p-2 arası
    b = secrets.randbelow(p - 2) + 1

    # 3) Elemanları hashleyip "körleme" (first blinding)
    blinded_A = []
    for x in set_A:
        hx = hash_to_int(x, p)
        X = pow(hx, a, p)
        blinded_A.append((x, X))  # (orijinal, körlenmiş)

    blinded_B = []
    for y in set_B:
        hy = hash_to_int(y, p)
        Y = pow(hy, b, p)
        blinded_B.append((y, Y))

    # 4) İkinci körleme (second blinding)
    double_B = []
    for (y, Y) in blinded_B:
        Y2 = pow(Y, a, p)
        double_B.append((y, Y2))

    double_A = []
    for (x, X) in blinded_A:
        X2 = pow(X, b, p)
        double_A.append((x, X2))

    # 5) Kesişimi H(z)^{ab} değerleri üzerinden bul
    values_A = {val for (_, val) in double_A}
    values_B = {val for (_, val) in double_B}

    intersection_blinded = values_A.intersection(values_B)

    # 6) Alice kendi tarafındaki map ile plaintext kesişimi çıkarsın
    map_val_to_x = {}
    for (x, val) in double_A:
        map_val_to_x[val] = x

    computed_intersection = {map_val_to_x[val] for val in intersection_blinded}

    # 7) Doğrulama için gerçek kesişimi hesapla
    real_intersection = set_A.intersection(set_B)

    return real_intersection, computed_intersection


def main():
    # ---- Burayı değiştirerek farklı senaryolar deneyeceğiz ----
    total_size = 10       # her setin boyu
    overlap_size = 3      # kesişimde kaç eleman olsun?

    set_A, set_B = generate_random_sets(total_size, overlap_size)

    print(f"Set A boyutu: {len(set_A)}")
    print(f"Set B boyutu: {len(set_B)}")
    print(f"Beklenen kesişim boyutu (teorik): {overlap_size}")

    real_inter, comp_inter = dh_psi(set_A, set_B)

    print("\nGerçek kesişim       :", real_inter)
    print("Gerçek kesişim boyutu:", len(real_inter))
    print("\nPSI ile bulunan kesişim       :", comp_inter)
    print("PSI ile bulunan kesişim boyutu:", len(comp_inter))

    if real_inter == comp_inter:
        print("\n✅ Prototip doğru çalışıyor (kesişimler eşleşiyor).")
    else:
        print("\n❌ Bir hata var, kesişimler farklı!")


if __name__ == "__main__":
    main()

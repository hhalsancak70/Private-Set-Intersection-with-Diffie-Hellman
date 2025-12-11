import hashlib
import secrets
import time
import csv
import statistics

# ============================
# Yardımcı fonksiyonlar
# ============================

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


# ============================
# Party sınıfı
# ============================

class Party:
    def __init__(self, name: str, p: int, g: int, elements):
        """
        name: 'Alice' veya 'Bob' gibi
        p, g: DH grup parametreleri
        elements: bu tarafın sahip olduğu elemanlar (set)
        """
        self.name = name
        self.p = p
        self.g = g
        self.elements = set(elements)
        self.secret = secrets.randbelow(p - 2) + 1  # gizli üs

    def blind_elements(self):
        """
        İlk körleme: (eleman, H(elem)^{secret}) listesi döner.
        """
        blinded = []
        for x in self.elements:
            hx = hash_to_int(x, self.p)
            X = pow(hx, self.secret, self.p)
            blinded.append((x, X))
        return blinded

    def second_blind(self, received_blinded):
        """
        İkinci körleme: karşı taraftan gelen (elem, val) listesinde
        val^secret hesaplar ve (elem, val^secret) listesi döner.
        """
        double = []
        for (y, Y) in received_blinded:
            Y2 = pow(Y, self.secret, self.p)
            double.append((y, Y2))
        return double


# ============================
# Protokol orkestrasyonu
# ============================

def dh_psi_with_parties(set_A, set_B):
    """
    Party sınıflarını kullanarak DH-PSI çalıştırır.
    Çıktı: (real_intersection, computed_intersection, elapsed_time)
    """

    # Ortak parametreler
    p = 2**127 - 1
    g = 5

    alice = Party("Alice", p, g, set_A)
    bob   = Party("Bob",   p, g, set_B)

    start = time.perf_counter()

    # 1) İlk körleme
    blinded_A = alice.blind_elements()
    blinded_B = bob.blind_elements()

    # 2) İkinci körleme
    double_B = alice.second_blind(blinded_B)  # H(y)^{ab}
    double_A = bob.second_blind(blinded_A)    # H(x)^{ab}

    # 3) Kesişim: Alice hesaplasın
    values_A = {val for (_, val) in double_A}
    values_B = {val for (_, val) in double_B}
    intersection_blinded = values_A.intersection(values_B)

    # Alice kendi tarafındaki map ile plaintext kesişimi bulur
    map_val_to_x = {val: x for (x, val) in double_A}
    computed_intersection = {map_val_to_x[val] for val in intersection_blinded}

    end = time.perf_counter()
    elapsed = end - start

    real_intersection = set_A.intersection(set_B)

    return real_intersection, computed_intersection, elapsed

def benchmark_runtime():
    """
    Farklı set boyları için DH-PSI süresini ölçer,
    her boy için birden fazla run yapıp ortalamasını alır,
    tablo olarak yazar ve results.csv dosyasına kaydeder.
    """

    sizes = [100, 500, 1000, 3000, 5000, 10000]
    overlap_ratio = 0.1  # %10 kesişim
    num_runs = 5          # her set boyu için kaç kez çalıştıralım?

    print("\n==========================")
    print("   DH-PSI Runtime Testi")
    print("==========================")
    print(f"{'Set Boyu':>10} | {'Kesişim':>10} | {'Ortalama Süre (s)':>18}")
    print("-" * 50)

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["set_size", "overlap_size", "avg_runtime_seconds"])

        for n in sizes:
            overlap = int(n * overlap_ratio)
            runtimes = []

            for _ in range(num_runs):
                set_A, set_B = generate_random_sets(n, overlap)
                real_inter, comp_inter, elapsed = dh_psi_with_parties(set_A, set_B)

                if real_inter != comp_inter:
                    print("❌ HATA: Kesişim yanlış!")
                    return

                runtimes.append(elapsed)

            avg_time = statistics.mean(runtimes)
            print(f"{n:>10} | {overlap:>10} | {avg_time:>18.6f}")

            writer.writerow([n, overlap, avg_time])




def main():
    print("Önce küçük bir doğruluk testi çalıştırıyoruz...\n")

    total_size = 50
    overlap_size = 10
    set_A, set_B = generate_random_sets(total_size, overlap_size)

    real_inter, comp_inter, t = dh_psi_with_parties(set_A, set_B)

    print("Gerçek kesişim boyutu:", len(real_inter))
    print("PSI kesişim boyutu  :", len(comp_inter))
    print(f"Protokol süresi: {t:.6f} saniye")

    if real_inter == comp_inter:
        print("✅ Doğruluk testi başarılı.\n")
    else:
        print("❌ Bir hata var!\n")
        return

    # ---- Artık benchmark'ı çalıştırıyoruz ----
    benchmark_runtime()



if __name__ == "__main__":
    main()

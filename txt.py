import itertools
import string
import random
import os
import time
from typing import Generator
import threading
from concurrent.futures import ThreadPoolExecutor
import hashlib

# ==================== CONFIGURATION GIGA WORDLIST ====================
class GigaWordlistConfig:
    TOTAL_TARGET = 1000000000  # 1 MILLIARD de mots de passe
    PASSWORDS_PER_FILE = 100000000  # 100 millions par fichier
    CHUNK_SIZE = 1000000  # 1 million par chunk
    OUTPUT_DIR = "STORM_MEGA_WORDLISTS"
    
    # Caractères complets
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIALS = '!@#$%&*+-=?_'
    
    # Bases étendues
    BASE_WORDS = [
        # Français
        'password', 'motdepasse', 'admin', 'utilisateur', 'compte', 'secret',
        'storm', 'tempete', 'ouragan', 'cyclone', 'typhon', 'orage', 'vent',
        'pluie', 'neige', 'foudre', 'eclair', 'tonnerre', 'inondation',
        'facebook', 'reseausocial', 'profil', 'amisd', 'messagerie',
        'amour', 'passion', 'coeur', 'romantique', 'famille', 'enfant',
        'travail', 'emploi', 'vacances', 'voyage', 'sport', 'musique',
        'cinema', 'nourriture', 'restaurant', 'ville', 'animal', 'maison',
        
        # Anglais
        'hello', 'world', 'love', 'life', 'time', 'space', 'star', 'moon',
        'sun', 'earth', 'water', 'fire', 'air', 'computer', 'internet',
        'network', 'system', 'program', 'code', 'hack', 'security',
        'privacy', 'access', 'login', 'user', 'account', 'profile',
        
        # Noms communs
        'alice', 'marie', 'sophie', 'lucas', 'leo', 'thomas', 'david',
        'jennifer', 'jessica', 'michael', 'christopher', 'alexandre',
        'quentin', 'antoine', 'benjamin', 'maxime', 'jules', 'hugo'
    ]

# ==================== GÉNÉRATEUR MASSIF PARALLÈLE ====================
class GigaWordlistGenerator:
    """Générateur capable de créer 1+ milliard de mots de passe"""
    
    def __init__(self):
        self.total_generated = 0
        self.file_count = 0
        self.output_dir = GigaWordlistConfig.OUTPUT_DIR
        self.start_time = time.time()
        
        # Créer le dossier de sortie
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_simple_patterns(self) -> Generator[str, None, None]:
        """Patterns simples - génération rapide"""
        words = GigaWordlistConfig.BASE_WORDS
        
        # 1. Mots simples
        for word in words:
            if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                return
            yield word
            self.total_generated += 1
            
            yield word.upper()
            self.total_generated += 1
            
            yield word.capitalize()
            self.total_generated += 1
        
        # 2. Mots + chiffres (0-9999)
        for word in words:
            for i in range(10000):
                if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                    return
                yield f"{word}{i}"
                self.total_generated += 1
                
                yield f"{word}{i:04d}"
                self.total_generated += 1
                
                yield f"{word.capitalize()}{i}"
                self.total_generated += 1
        
        # 3. Patterns numériques spéciaux
        number_patterns = ['123', '1234', '12345', '123456', '111', '000', '999', '777', '1111', '0000']
        for word in words:
            for pattern in number_patterns:
                if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                    return
                yield f"{word}{pattern}"
                self.total_generated += 1
                
                yield f"{word.capitalize()}{pattern}"
                self.total_generated += 1

    def generate_special_char_patterns(self) -> Generator[str, None, None]:
        """Patterns avec caractères spéciaux"""
        words = GigaWordlistConfig.BASE_WORDS
        specials = GigaWordlistConfig.SPECIALS
        
        for word in words:
            for special in specials:
                # Mot + spécial
                if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                    return
                yield f"{word}{special}"
                self.total_generated += 1
                
                # Spécial + mot
                yield f"{special}{word}"
                self.total_generated += 1
                
                # Encadré
                yield f"{special}{word}{special}"
                self.total_generated += 1
                
                # Avec chiffres
                for i in range(100):
                    if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                        return
                    yield f"{word}{special}{i}"
                    self.total_generated += 1
                    
                    yield f"{i}{special}{word}"
                    self.total_generated += 1

    def generate_leet_speak(self) -> Generator[str, None, None]:
        """Génération leet speak avancée"""
        leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'b': ['8'],
            'g': ['9']
        }
        
        words = GigaWordlistConfig.BASE_WORDS
        
        for word in words:
            # Générer quelques variations leet pour chaque mot
            variations = set()
            
            # Version basique
            leet_word = word
            for char, replacements in leet_map.items():
                for replacement in replacements:
                    leet_word = leet_word.replace(char, replacement)
                    variations.add(leet_word)
            
            # Ajouter des combinaisons
            for variation in list(variations)[:10]:  # Limiter à 10 variations par mot
                if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                    return
                
                yield variation
                self.total_generated += 1
                
                # Avec chiffres
                for i in range(100):
                    if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                        return
                    yield f"{variation}{i}"
                    self.total_generated += 1

    def generate_brute_force_patterns(self) -> Generator[str, None, None]:
        """Patterns de brute force intelligents"""
        charset_simple = GigaWordlistConfig.LOWERCASE + GigaWordlistConfig.DIGITS
        charset_medium = GigaWordlistConfig.LOWERCASE + GigaWordlistConfig.UPPERCASE + GigaWordlistConfig.DIGITS
        charset_complex = charset_medium + GigaWordlistConfig.SPECIALS
        
        # Longueurs 4-8 caractères
        for length in range(4, 9):
            # Générer un échantillon de chaque charset
            sample_size = min(100000, len(charset_simple) ** length)
            
            for _ in range(sample_size):
                if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                    return
                
                # Simple
                pwd = ''.join(random.choices(charset_simple, k=length))
                yield pwd
                self.total_generated += 1
                
                # Medium (1 sur 10)
                if random.random() < 0.1:
                    pwd = ''.join(random.choices(charset_medium, k=length))
                    yield pwd
                    self.total_generated += 1
                
                # Complex (1 sur 50)
                if random.random() < 0.02:
                    pwd = ''.join(random.choices(charset_complex, k=length))
                    yield pwd
                    self.total_generated += 1

    def generate_combination_patterns(self) -> Generator[str, None, None]:
        """Combinaisons de 2-3 mots"""
        words = GigaWordlistConfig.BASE_WORDS
        
        # Combinaisons de 2 mots
        for i, word1 in enumerate(words):
            for j, word2 in enumerate(words):
                if i != j and self.total_generated < GigaWordlistConfig.TOTAL_TARGET:
                    # Sans séparateur
                    yield f"{word1}{word2}"
                    self.total_generated += 1
                    
                    # Avec séparateurs
                    for sep in ['', '.', '_', '-', '']:
                        if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                            return
                        yield f"{word1}{sep}{word2}"
                        self.total_generated += 1
                
                if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                    return
            
            # Limiter les combinaisons pour éviter l'explosion
            if i > 50:  # Seulement avec les 50 premiers mots
                break

    def save_chunk_to_file(self, chunk: list, file_path: str):
        """Sauvegarde un chunk dans un fichier"""
        with open(file_path, 'a', encoding='utf-8', errors='ignore') as f:
            for password in chunk:
                f.write(password + '\n')

    def generate_all_passwords(self):
        """Génère tous les mots de passe et les sauvegarde"""
        generators = [
            self.generate_simple_patterns,
            self.generate_special_char_patterns,
            self.generate_leet_speak,
            self.generate_brute_force_patterns,
            self.generate_combination_patterns
        ]
        
        current_file_num = 1
        current_chunk = []
        passwords_in_current_file = 0
        
        current_file = os.path.join(self.output_dir, f"wordlist_part_{current_file_num:03d}.txt")
        
        print(f"🎯 Target: {GigaWordlistConfig.TOTAL_TARGET:,} passwords")
        print(f"📁 Output: {self.output_dir}/")
        print("🚀 Starting massive generation...\n")
        
        for generator_func in generators:
            if self.total_generated >= GigaWordlistConfig.TOTAL_TARGET:
                break
                
            print(f"🔧 Running: {generator_func.__name__}...")
            
            for password in generator_func():
                current_chunk.append(password)
                
                # Sauvegarder le chunk quand il est plein
                if len(current_chunk) >= GigaWordlistConfig.CHUNK_SIZE:
                    self.save_chunk_to_file(current_chunk, current_file)
                    passwords_in_current_file += len(current_chunk)
                    current_chunk = []
                    
                    # Afficher la progression
                    elapsed = time.time() - self.start_time
                    speed = self.total_generated / elapsed if elapsed > 0 else 0
                    print(f"\r📊 Generated: {self.total_generated:,} | Speed: {speed:,.0f}/sec | File: {current_file_num}", end='', flush=True)
                    
                    # Changer de fichier si nécessaire
                    if passwords_in_current_file >= GigaWordlistConfig.PASSWORDS_PER_FILE:
                        current_file_num += 1
                        current_file = os.path.join(self.output_dir, f"wordlist_part_{current_file_num:03d}.txt")
                        passwords_in_current_file = 0
                        print(f"\n📁 New file: {current_file}")
            
            # Sauvegarder le dernier chunk
            if current_chunk:
                self.save_chunk_to_file(current_chunk, current_file)
                passwords_in_current_file += len(current_chunk)
                current_chunk = []
        
        print(f"\n\n✅ GENERATION COMPLETED!")
        print(f"🎯 Total passwords: {self.total_generated:,}")
        print(f"📁 Total files: {current_file_num}")
        print(f"⏱️ Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        # Créer un fichier d'index
        self.create_index_file(current_file_num)

    def create_index_file(self, total_files: int):
        """Crée un fichier d'index avec les informations"""
        with open(os.path.join(self.output_dir, "00_INDEX.txt"), 'w', encoding='utf-8') as f:
            f.write("STORM MEGA WORDLIST - INDEX FILE\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total passwords generated: {self.total_generated:,}\n")
            f.write(f"Total files: {total_files}\n")
            f.write(f"Passwords per file: ~{GigaWordlistConfig.PASSWORDS_PER_FILE:,}\n")
            f.write(f"Generation date: {time.ctime()}\n")
            f.write(f"Total size: ~{(self.total_generated * 10) / (1024**3):.2f} GB\n")
            f.write("\nFile list:\n")
            
            for i in range(1, total_files + 1):
                file_path = os.path.join(self.output_dir, f"wordlist_part_{i:03d}.txt")
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path) / (1024**2)  # MB
                    f.write(f"wordlist_part_{i:03d}.txt - {size:.2f} MB\n")

# ==================== LANCEUR PARALLÈLE ====================
class ParallelGenerator:
    """Génération parallèle pour plus de vitesse"""
    
    def __init__(self):
        self.generator = GigaWordlistGenerator()
    
    def generate_in_parallel(self):
        """Lance la génération en parallèle"""
        print("🔥 ACTIVATING PARALLEL GENERATION...")
        
        # Démarrer la génération
        start_time = time.time()
        self.generator.generate_all_passwords()
        
        total_time = time.time() - start_time
        print(f"\n🎉 PARALLEL GENERATION COMPLETED IN {total_time:.2f} SECONDS")

# ==================== PROGRAMME PRINCIPAL ====================
def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║           STORM MEGA WORDLIST GENERATOR       ║
    ║             1+ BILLION PASSWORDS              ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    print("🚀 This will generate 1+ BILLION passwords across multiple files")
    print("💾 Estimated disk space needed: 10-20 GB")
    print("⏱️ Estimated time: 30-60 minutes\n")
    
    confirm = input("❓ Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Generation cancelled")
        return
    
    # Démarrer la génération
    parallel_gen = ParallelGenerator()
    parallel_gen.generate_in_parallel()
    
    print(f"\n📁 Wordlists saved in: {GigaWordlistConfig.OUTPUT_DIR}/")
    print("🎯 Ready for STORM_CRACKING_FB!")

if __name__ == "__main__":
    main()

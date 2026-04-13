#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all dependencies and configurations are correct
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def check_python_packages():
    print_header("Checking Python Packages")
    required_packages = [
        'flask', 'flask_cors', 'pandas', 'numpy', 'scipy',
        'statsmodels', 'prophet', 'tensorflow', 'sklearn', 'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All Python packages installed")
        return True

def check_csv_files():
    print_header("Checking CSV Data Files")
    csv_files = list(Path('.').glob('*.csv'))
    csv_files = [f for f in csv_files if 'summary' not in f.name.lower() and 'analysis' not in f.name.lower()]
    
    if len(csv_files) > 0:
        print(f"✅ Found {len(csv_files)} cryptocurrency data files")
        print(f"   Sample: {', '.join([f.stem for f in csv_files[:5]])}")
        return True
    else:
        print("❌ No CSV data files found")
        return False

def check_frontend_setup():
    print_header("Checking Frontend Setup")
    frontend_dir = Path('asset-forecaster-pro-main')
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print(f"✅ Frontend directory exists")
    
    # Check package.json
    package_json = frontend_dir / 'package.json'
    if package_json.exists():
        print("✅ package.json found")
    else:
        print("❌ package.json not found")
        return False
    
    # Check node_modules
    node_modules = frontend_dir / 'node_modules'
    if node_modules.exists():
        print("✅ node_modules installed")
    else:
        print("⚠️  node_modules not found - run 'npm install' in frontend directory")
        return False
    
    # Check .env file
    env_file = frontend_dir / '.env'
    if env_file.exists():
        print("✅ .env file configured")
    else:
        print("⚠️  .env file not found")
    
    return True

def check_api_file():
    print_header("Checking API Backend")
    if Path('api.py').exists():
        print("✅ api.py found")
        return True
    else:
        print("❌ api.py not found")
        return False

def check_node_npm():
    print_header("Checking Node.js and npm")
    try:
        node_version = subprocess.check_output(['node', '--version'], stderr=subprocess.STDOUT, text=True).strip()
        print(f"✅ Node.js {node_version}")
    except:
        print("❌ Node.js not found - install from https://nodejs.org/")
        return False
    
    try:
        npm_version = subprocess.check_output(['npm', '--version'], stderr=subprocess.STDOUT, text=True).strip()
        print(f"✅ npm {npm_version}")
        return True
    except:
        print("❌ npm not found")
        return False

def main():
    print("\n" + "🔍 CRYPTOCURRENCY ANALYSIS PLATFORM - SETUP VERIFICATION".center(60))
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Packages", check_python_packages),
        ("CSV Data Files", check_csv_files),
        ("API Backend", check_api_file),
        ("Node.js & npm", check_node_npm),
        ("Frontend Setup", check_frontend_setup),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} checks passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to run the application.")
        print("\nNext steps:")
        print("  1. Run: python api.py (in one terminal)")
        print("  2. Run: cd asset-forecaster-pro-main && npm run dev (in another terminal)")
        print("  3. Or simply double-click: start_app.bat")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install Python packages: pip install -r requirements.txt")
        print("  - Install frontend packages: cd asset-forecaster-pro-main && npm install")
        print("  - Install Node.js from: https://nodejs.org/")
    
    print()

if __name__ == "__main__":
    main()

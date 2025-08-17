#!/usr/bin/env python3
"""
Streamlit AgGrid SDK Quick Build Script
"""

import subprocess
import sys
from pathlib import Path
import shutil
import platform


def run_cmd(cmd, cwd=None, timeout=300):
    """Run command"""
    try:
        use_shell = platform.system() == "Windows"
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            shell=use_shell,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Command failed: {e}\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return False, f"Command timeout: {' '.join(cmd)}"
    except Exception as e:
        return False, f"Exception: {e}"


def build_frontend():
    """Build frontend"""
    frontend_dir = Path("st_aggrid/frontend")
    if not frontend_dir.exists():
        print("⚠️ Frontend directory does not exist, skipping frontend build")
        return True

    # Check Node.js
    success, output = run_cmd(["node", "--version"])
    if not success:
        print("⚠️ Node.js not available, skipping frontend build")
        return True

    print(f"📦 Node.js: {output.strip()}")

    # Choose package manager
    if (frontend_dir / "yarn.lock").exists():
        install_cmd = ["yarn", "install"]
        build_cmd = ["yarn", "build"]
        pkg_mgr = "yarn"
    else:
        install_cmd = ["npm", "install"]
        build_cmd = ["npm", "run", "build"]
        pkg_mgr = "npm"

    print(f"🔧 Building frontend using {pkg_mgr}...")

    # Install dependencies
    success, output = run_cmd(install_cmd, cwd=frontend_dir, timeout=300)
    if not success:
        print(f"❌ Dependency installation failed: {output}")
        return False

    # Build
    success, output = run_cmd(build_cmd, cwd=frontend_dir, timeout=600)
    if not success:
        print(f"❌ Frontend build failed: {output}")
        return False

    print("✅ Frontend build completed")
    return True


def build_python():
    """Build Python package"""
    print("🔧 Building Python package...")

    # Prepare dist directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # Try PEP 517 build
    success, output = run_cmd([sys.executable, "-m", "pip", "install", "-U", "build"])
    if success:
        success, output = run_cmd([sys.executable, "-m", "build"])
        if success:
            print("✅ Python package build completed (PEP 517)")
            return True

    # Fallback to setup.py
    if Path("setup.py").exists():
        success, output = run_cmd([sys.executable, "setup.py", "bdist_wheel"])
        if success:
            print("✅ Python package build completed (setup.py)")
            return True

    print(f"❌ Python package build failed: {output}")
    return False


def main():
    """Main function"""
    print("🚀 Streamlit AgGrid SDK Quick Build")
    print("=" * 40)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)

    print(f"✅ Python: {sys.version.split()[0]}")

    # Build frontend
    if "--skip-frontend" not in sys.argv:
        if not build_frontend():
            if "--strict" in sys.argv:
                sys.exit(1)
            print("⚠️ Frontend build failed, continuing with Python package build...")
    else:
        print("⏭️ Skipping frontend build")

    # Build Python package
    if "--skip-python" not in sys.argv:
        if not build_python():
            sys.exit(1)
    else:
        print("⏭️ Skipping Python package build")

    # Show results
    wheels = list(Path("dist").glob("*.whl"))
    if wheels:
        print(f"\n🎉 Build completed! Generated {len(wheels)} files:")
        for wheel in wheels:
            print(f"  📦 {wheel.name}")
    else:
        print("\n⚠️ No generated wheel files found")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Usage: python build_sdk.py [options]

Options:
  --skip-frontend    Skip frontend build
  --skip-python      Skip Python package build
  --strict           Stop on frontend build failure
  --help, -h         Show help

Examples:
  python build_sdk.py                 # Full build
  python build_sdk.py --skip-frontend # Build Python package only
        """)
        sys.exit(0)

    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Build interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

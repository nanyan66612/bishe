import subprocess, tempfile, os

def run_c_code(code, ipt, opt):
    try:
        with tempfile.NamedTemporaryFile(suffix='.c', delete=False) as f:
            f.write(code.encode())
            c = f.name
        exe = c[:-2]
        # 编译
        cp = subprocess.run(['gcc',c,'-o',exe], capture_output=True, timeout=3)
        if cp.returncode !=0: return 'CE'
        # 运行
        rp = subprocess.run([exe], input=ipt, capture_output=True, text=True, timeout=3)
        # 比对
        return 'AC' if rp.stdout.strip() == opt.strip() else 'WA'
    except:
        return 'RE'
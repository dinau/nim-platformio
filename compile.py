from os import system, path
from shutil import copyfile
from pathlib import Path

Import("env")

src = Path(env.subst("$PROJECT_SRC_DIR"))

if not path.exists(src/'panicoverride.nim'):
  copyfile(Path().parent/'panicoverride.nim', src/'panicoverride.nim')

libdeps = env.subst("$PROJECT_LIBDEPS_DIR/$PIOENV")

cpu = "avr"
if "espressif" in env.subst("$PIOPLATFORM"):
  cpu = "esp"

flags = (
  f"--path:{libdeps} "
  f"--path:{libdeps}/nim-arduino "
  f"--nimcache:{src/'nimcache'} "
  "--compileOnly "
  f"--cpu:{cpu} "
#  "--deadCodeElim "
#"--os:standalone "
  "--os:any "
  "--noMain "
  "--gc:arc "
#  "--mm:none " # nim-1.6.8 or later
  "--stacktrace:off "
  "--profiler:off "
  "-d:useMalloc "
  "--exceptions:goto "
  "-d:noSignalHandler "
  "--opt:size "
  "-d:danger "
)

result = system(f"nim cpp {flags} {src/'main'}")
if result != 0:
  exit(result)

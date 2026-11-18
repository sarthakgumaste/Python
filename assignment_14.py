import logging
import logging.config
import logging.handlers
import os
import tempfile

LOG_DIR = tempfile.mkdtemp(prefix="logdemo_")


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")

def demo_levels():
    section("1. Levels (threshold = DEBUG, everything shows)")
    log = logging.getLogger("levels")
    log.setLevel(logging.DEBUG)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
    log.addHandler(h)
    log.propagate = False

    log.debug("detailed info for developers")
    log.info("normal progress message")
    log.warning("something unexpected, still working")
    log.error("an operation failed")
    log.critical("the program may not continue")

    print("--- raise threshold to WARNING: DEBUG and INFO are hidden ---")
    log.setLevel(logging.WARNING)
    log.debug("you will NOT see this")
    log.info("you will NOT see this either")
    log.warning("but you WILL see this warning")

def demo_formatter():
    section("2. Formatter (time | logger | level | function | message)")
    log = logging.getLogger("format")
    log.setLevel(logging.INFO)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%H:%M:%S"))
    log.addHandler(h)
    log.propagate = False
    log.info("Formatted entry with time, place and level")

def demo_handlers():
    section("3. Two handlers: console (INFO+) and file (WARNING+)")
    path = os.path.join(LOG_DIR, "app.log")
    log = logging.getLogger("handlers")
    log.setLevel(logging.DEBUG)
    log.propagate = False

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("CONSOLE  %(levelname)s - %(message)s"))

    file_h = logging.FileHandler(path)
    file_h.setLevel(logging.WARNING)
    file_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))

    log.addHandler(console)
    log.addHandler(file_h)

    log.debug("debug: goes nowhere (both handlers ignore it)")
    log.info("info: console only")
    log.warning("warning: console AND file")
    log.error("error: console AND file")

    file_h.flush()
    print("\nContents of app.log (only WARNING and above):")
    with open(path) as f:
        for line in f:
            print("  FILE   ", line.rstrip())

def demo_rotation():
    section("4. RotatingFileHandler (max 200 bytes, keep 2 backups)")
    path = os.path.join(LOG_DIR, "rotate.log")
    log = logging.getLogger("rotate")
    log.setLevel(logging.INFO)
    log.propagate = False
    h = logging.handlers.RotatingFileHandler(path, maxBytes=200, backupCount=2)
    h.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(h)
    for i in range(1, 21):
        log.info("rotating entry number %d", i)
    h.close()
    print("Files created:", sorted(f for f in os.listdir(LOG_DIR) if f.startswith("rotate")))

def demo_hierarchy():
    section("5. Logger hierarchy (shop -> shop.cart, shop.pay)")
    parent = logging.getLogger("shop")
    parent.setLevel(logging.INFO)
    parent.propagate = False
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
    parent.addHandler(h)

    logging.getLogger("shop.cart").info("item added to cart")
    logging.getLogger("shop.pay").info("payment accepted")
    logging.getLogger("shop.pay").debug("hidden: parent level is INFO")

def demo_exception():
    section("6. logger.exception() records the traceback")
    log = logging.getLogger("errors")
    log.propagate = False
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(h)
    try:
        10 / 0
    except ZeroDivisionError:
        log.exception("Division failed")

class HideSecrets(logging.Filter):
    def filter(self, record):
        return "password" not in record.getMessage().lower()


def demo_filter():
    section("7. Filter (blocks messages containing 'password')")
    log = logging.getLogger("secure")
    log.setLevel(logging.INFO)
    log.propagate = False
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    h.addFilter(HideSecrets())
    log.addHandler(h)
    log.info("user rahul logged in")
    log.info("password for rahul is 1234")      # blocked
    log.info("user rahul opened dashboard")

def demo_lazy_and_extra():
    section("8. Lazy %s formatting and extra={...} fields")
    log = logging.getLogger("extras")
    log.setLevel(logging.INFO)
    log.propagate = False
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)s user=%(user)s %(message)s"))
    log.addHandler(h)
    log.info("order %d placed, total Rs.%.2f", 42, 1999.5, extra={"user": "rahul"})

def demo_dictconfig():
    section("9. dictConfig (whole setup in one dictionary)")
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"short": {"format": "%(levelname)s:%(name)s:%(message)s"}},
        "handlers": {"console": {"class": "logging.StreamHandler",
                                 "formatter": "short", "level": "INFO"}},
        "loggers": {"configured": {"handlers": ["console"], "level": "INFO",
                                   "propagate": False}},
    }
    logging.config.dictConfig(cfg)
    logging.getLogger("configured").info("configured entirely from a dict")


if __name__ == "__main__":
    demo_levels()
    demo_formatter()
    demo_handlers()
    demo_rotation()
    demo_hierarchy()
    demo_exception()
    demo_filter()
    demo_lazy_and_extra()
    demo_dictconfig()
    print(f"\nLog files were written to: {LOG_DIR}")
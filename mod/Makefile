# ------------------------------------------------------ #
# Makefile for Quake 2 Mod: q2fun                        #
#                                                        #
# Just type "make" to build game.so                      #
# Type "make install" to copy to the game directory      #
# Type "make clean" to clean build artifacts             #
# ------------------------------------------------------ #

# Mod name - this becomes the directory name in the Q2 install
MOD_NAME := q2fun

# Yamagi Quake II install directory
# Override with: make Q2DIR=/path/to/quake2
Q2DIR := $(HOME)/.yq2

CC := gcc
YQ2ARCH := $(shell uname -m)
YQ2OSTYPE := $(shell uname -s | tr '[:upper:]' '[:lower:]')

CFLAGS := -O2 -Wall -fPIC -Wno-unused-result -Wno-unused-parameter \
	-Wno-missing-field-initializers -Wno-sign-compare \
	-DYQ2ARCH=\"$(YQ2ARCH)\" -DYQ2OSTYPE=\"$(YQ2OSTYPE)\" \
	-DNEED_STRLCPY -DNEED_STRLCAT
LDFLAGS := -shared -lm

# Debug build: make DEBUG=1
ifdef DEBUG
CFLAGS := -O0 -g -Wall -fPIC -Wno-unused-result -Wno-unused-parameter \
	-Wno-missing-field-initializers -Wno-sign-compare \
	-DYQ2ARCH=\"$(YQ2ARCH)\" -DYQ2OSTYPE=\"$(YQ2OSTYPE)\" -DDEBUG \
	-DNEED_STRLCPY -DNEED_STRLCAT
endif

BUILDDIR := build
BINDIR := release

# Source files
GAME_SRCS := \
	src/common/shared/flash.c \
	src/common/shared/rand.c \
	src/common/shared/shared.c \
	src/game/g_ai.c \
	src/game/g_chase.c \
	src/game/g_cmds.c \
	src/game/g_combat.c \
	src/game/g_func.c \
	src/game/g_items.c \
	src/game/g_main.c \
	src/game/g_misc.c \
	src/game/g_monster.c \
	src/game/g_phys.c \
	src/game/g_spawn.c \
	src/game/g_svcmds.c \
	src/game/g_target.c \
	src/game/g_trigger.c \
	src/game/g_turret.c \
	src/game/g_utils.c \
	src/game/g_weapon.c \
	src/game/monster/berserker/berserker.c \
	src/game/monster/boss2/boss2.c \
	src/game/monster/boss3/boss3.c \
	src/game/monster/boss3/boss31.c \
	src/game/monster/boss3/boss32.c \
	src/game/monster/brain/brain.c \
	src/game/monster/chick/chick.c \
	src/game/monster/flipper/flipper.c \
	src/game/monster/float/float.c \
	src/game/monster/flyer/flyer.c \
	src/game/monster/gladiator/gladiator.c \
	src/game/monster/gunner/gunner.c \
	src/game/monster/hover/hover.c \
	src/game/monster/infantry/infantry.c \
	src/game/monster/insane/insane.c \
	src/game/monster/medic/medic.c \
	src/game/monster/misc/move.c \
	src/game/monster/mutant/mutant.c \
	src/game/monster/parasite/parasite.c \
	src/game/monster/soldier/soldier.c \
	src/game/monster/supertank/supertank.c \
	src/game/monster/tank/tank.c \
	src/game/player/client.c \
	src/game/player/hud.c \
	src/game/player/trail.c \
	src/game/player/view.c \
	src/game/player/weapon.c \
	src/game/savegame/savegame.c \
	src/game/g_ctf.c \
	src/lithium/lithium.c \
	src/lithium/l_admin.c \
	src/lithium/l_display.c \
	src/lithium/l_fragtrak.c \
	src/lithium/l_gslog.c \
	src/lithium/l_hook.c \
	src/lithium/l_hscore.c \
	src/lithium/l_mapqueue.c \
	src/lithium/l_menu.c \
	src/lithium/l_net.c \
	src/lithium/l_nocamp.c \
	src/lithium/l_obit.c \
	src/lithium/l_pack.c \
	src/lithium/l_rune.c \
	src/lithium/l_var.c \
	src/lithium/l_vote.c \
	src/lithium/net.c \
	src/lithium/strl.c \
	src/lithium/zbotcheck.c \
	src/lithium/p_menu.c

GAME_OBJS := $(patsubst %.c,$(BUILDDIR)/%.o,$(GAME_SRCS))

# Default target
all: $(BINDIR)/game.so
	@echo ""
	@echo "=== Build complete: $(BINDIR)/game.so ==="
	@echo "Run 'make install' to install to $(Q2DIR)/$(MOD_NAME)/"
	@echo ""

$(BINDIR)/game.so: $(GAME_OBJS)
	@echo "===> LD $@"
	@mkdir -p $(BINDIR)
	$(CC) $(LDFLAGS) $(GAME_OBJS) -o $@

$(BUILDDIR)/%.o: %.c
	@echo "===> CC $<"
	@mkdir -p $(dir $@)
	$(CC) -c $(CFLAGS) -o $@ $<

# Install to Yamagi Quake II directory
install: $(BINDIR)/game.so
	@mkdir -p $(Q2DIR)/$(MOD_NAME)
	cp $(BINDIR)/game.so $(Q2DIR)/$(MOD_NAME)/game.so
	@echo "Installed to $(Q2DIR)/$(MOD_NAME)/game.so"
	@echo "Launch with: quake2 +set game $(MOD_NAME)"

clean:
	rm -rf $(BUILDDIR) $(BINDIR)

# Rebuild everything
rebuild: clean all

.PHONY: all install clean rebuild

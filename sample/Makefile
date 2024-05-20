default: all
.PHONY: default

# Cプログラム作成用Makefileのテンプレです

MAKEFLAGS ?= -j$(shell nproc)

INTERMEDIATE := ./build
$(shell mkdir -p $(INTERMEDIATE))

CSRCDIR := src
CSRC := $(wildcard $(addprefix $(CSRCDIR)/,*.c))
OBJS := $(CSRC:$(CSRCDIR)/%.c=$(INTERMEDIATE)/%.o)
DEPE := $(OBJS:%.o=%.d)
program := $(INTERMEDIATE)/program

CC := gcc
CFLAGS := -O2 -MMD -g $(INCLUDE)

.PHONY: all run clean

# 実行する
all: $(program)
run: all
	./$(program)
# コンパイルする
$(program): $(OBJS)
	$(CC) -o $@ $^
$(OBJS): build/%.o: $(CSRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $(filter %.c,$^) -MF $(patsubst %.o,%.d,$@)

# 中間ファイルをすべて消去する
clean:
	rm -rf $(INTERMEDIATE) $(program)
	
-include $(DEPE)
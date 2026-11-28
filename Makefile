WIT := wit
BSDIFF := bsdiff
PYTHON := python3

# Currently, just causes the name to be changed when building the iso, but has
# no effect on the name in Archipelago.
COPY_FLAGS := --name="Pokemon Battle Revolution Archipelago"

ISO_IN := pbr_vanilla.iso
ISO_OUT := pbr_patched.iso
ISO_EXTRACT_DIR := ./PBR_EXTRACT
ISO_PATCHED_DIR := ./PBR_PATCHED

DOL_PATH := DATA/sys/main.dol
VANILLA_DOL := $(ISO_EXTRACT_DIR)/$(DOL_PATH)
PATCHED_DOL := $(ISO_PATCHED_DIR)/$(DOL_PATH)
XML_PATCH_DOL := ap_pbr_patch.xml

PATCH_DIR := ./patches
DOL_PATCH_DIR := $(PATCH_DIR)/dol
BSDIFF_PATCH_DIR := $(PATCH_DIR)/bsdiff

SETS_DIR := ./sets
SUBSET_DIRS := $(wildcard $(SETS_DIR)/*)
PK4_SETS := $(foreach subset_dir, $(SUBSET_DIRS), $(wildcard $(subset_dir)/*.pk4))
PYTHON_SETS := $(foreach subset_dir, $(SUBSET_DIRS), $(notdir $(subset_dir)))
CLEAN_SETS := $(foreach sets_name, $(PYTHON_SETS), $(sets_name)_sets.py)
PK4_TO_PY_SET := pk4_recombinator.py

BSDIFF_OUT_DIR := ./BSDIFFS
BSDIFF_DOL := $(BSDIFF_OUT_DIR)/$(notdir $(DOL_PATH)).bsdiff

$(ISO_EXTRACT_DIR): $(ISO_IN)
	$(WIT) EXTRACT $(ISO_IN) $@

$(ISO_PATCHED_DIR): $(ISO_EXTRACT_DIR)
	cp -r $< $@

$(BSDIFF_OUT_DIR):
	mkdir -p $@

$(XML_PATCH_DOL): $(DOL_PATCH_FILES)
	cat $^ > $(XML_PATCH_DOL)

$(PATCHED_DOL): $(ISO_PATCHED_DIR) $(XML_PATCH_DOL)
	$(WIT) dolpatch $(VANILLA_DOL) xml=$(XML_PATCH_DOL) --dest $@ --overwrite

$(ISO_OUT): $(PATCHED_DOL)
	$(WIT) copy $(ISO_PATCHED_DIR) $@ --overwrite $(COPY_FLAGS)

$(BSDIFF_DOL): $(ISO_EXTRACT_DIR) $(PATCHED_DOL)
	$(BSDIFF) $(VANILLA_DOL) $(PATCHED_DOL) $(BSDIFF_DOL) 

.PHONY: bsdiffs
bsdiffs: $(BSDIFF_OUT_DIR) $(BSDIFF_DOL)

.PHONY: patched_iso
patched_iso: $(ISO_OUT)

.PHONY: fix_set_names
fix_set_names: $(SUBSET_DIRS)

# Trim any 'fat' from the pk4
.PHONY: $(SUBSET_DIRS)
$(SUBSET_DIRS):
	rename -v -f 's/($(subst /,\/,$@)\/)(.{5}).*(\.pk4)/$$1$$2$$3/' $@/*.pk4

$(PYTHON_SETS):
	echo Making Sets For: $@
	@$(PYTHON) $(PK4_TO_PY_SET) $@ $(filter $(SETS_DIR)/$@/%.pk4, $(PK4_SETS))

.PHONY: sets
sets: $(PYTHON_SETS)

.PHONY: clean
clean:
	rm -rf $(ISO_EXTRACT_DIR) $(ISO_PATCHED_DIR) $(BSDIFF_OUT_DIR) $(XML_PATCH_DOL) $(ISO_OUT) $(CLEAN_SETS)
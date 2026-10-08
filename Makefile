WIT := wit
BSDIFF := bsdiff

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
DOL_PATCH_FILES := $(foreach file,$(wildcard $(DOL_PATCH_DIR)/*.xml),$(file))
BSDIFF_PATCH_FILES := $(foreach file,$(wildcard $(BSDIFF_PATCH_DIR)/*.bsdiff),$(file))

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

.PHONY: clean
clean:
	rm -rf $(ISO_EXTRACT_DIR) $(ISO_PATCHED_DIR) $(BSDIFF_OUT_DIR) $(XML_PATCH_DOL) $(ISO_OUT)
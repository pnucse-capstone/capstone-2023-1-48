# SSD simulator

## I/O Trace
- `iotrace_simluation.csv`
- Length of I/O Trace : 3939773
- Unique Logical Page Address of I/O trace : 132920
  - Total Number of Pages MUST LARGER THAN `132920 / (1-ssd_gc_threshold)`
    - Assume that ssd_gc_threshold equals to 0.3, 
    - Total Number of Pages must be larger than 189,885
    - Otherwise, `MEMORY ERROR` would occur

## SSD Configuration
- Page per Block = 128
- Block per SSD = 3000
- Total Number of Pages = 128 * 2000 = 384000
- Page size = 4KB
- SSD size = 1024MB

## GC Trigger
- entire blocks' empty page < `ssd_gc_threshold`

## Garbage Collection Algorithm 
1. Find the victim block with most `INVALID` pages
2. Relocate victim block's `WRITTEN` pages to the *best writable page*
   - *Best writable page* means that page with the most `EMPTY` pages
     - If the amount of the most `EMPTY` pages equals to 0, It indicates `MEMORY ERROR`
   - Increase `Additional Write` with each relocation
3. Erase victim block's data
   - Set block's entire pages' state `EMPTY`
   - Set block's entire pages' Logical Page Address `NONE`

## Note
- No Wear-Leveling

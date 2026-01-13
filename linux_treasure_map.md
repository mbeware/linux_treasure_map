# linux treasure map

## Core Kernel Infrastructure

### locking
The locking subsystem provides the synchronization primitives (spinlocks, mutexes, rwlocks, seqlocks, etc.) that protect shared data structures inside the kernel. Its job is to balance correctness and performance: prevent races without destroying scalability on large systems. Most kernel bugs eventually reduce to locking mistakes.

### RCU
RCU (Read-Copy-Update) is a synchronization mechanism optimized for read-heavy workloads. Readers run without locks, while updaters create new versions of data and retire old ones after a grace period. It underpins critical paths like networking, VFS, and scheduler internals.

### workqueue
Workqueues provide a deferred execution mechanism for running tasks in process context instead of interrupt context. They are heavily used by drivers and core subsystems to offload slow or blocking work while maintaining ordering and CPU affinity guarantees.

### slab
The slab allocator manages kernel memory caches for frequently used objects. It reduces allocation overhead, improves cache locality, and provides debugging hooks for memory corruption. Slab behavior directly impacts performance and memory fragmentation.

### memblock
Memblock is the early-boot memory allocator used before the full page allocator is initialized. It tracks physical memory regions, reserved areas, and firmware-provided layouts. If memblock goes wrong, the kernel usually never reaches userspace.

### debugobjects
Debugobjects track the lifecycle of kernel objects to catch misuse such as double initialization or use-after-free. They are a defensive subsystem aimed at developers, trading runtime overhead for earlier detection of subtle bugs.

### bitmap
The bitmap helpers provide efficient operations on bit arrays, used everywhere from CPU masks to block allocation maps. They are low-level but performance-critical, especially in scheduler and memory management code.

### nolibc
nolibc is a minimal C library intended for kernel-adjacent environments like early boot, selftests, and tiny user programs. It avoids pulling in glibc while still providing essential syscalls and helpers.

### printk
printk is the kernel’s logging facility. It handles message formatting, log levels, buffering, and delivery to consoles and userspace. Changes here affect debuggability, performance, and system reliability during failures.

### lkmm
The Linux Kernel Memory Model (LKMM) formally defines how memory ordering works across CPUs and architectures. It provides a shared mental model for developers writing lock-free or weakly ordered code.

## Scheduling, CPU, and Process Management

### scheduler
The scheduler decides which task runs on which CPU and for how long. It balances fairness, throughput, latency, and power efficiency. Scheduler changes are among the most delicate and visible kernel modifications.

### sched_ext
sched_ext is an extension framework allowing custom scheduling policies to be implemented outside the core scheduler. It enables experimentation without destabilizing the default scheduling logic.

### futex
Futexes (fast userspace mutexes) provide a low-level synchronization primitive shared between userspace and the kernel. They allow uncontended locking to stay in userspace while still supporting kernel-assisted blocking when needed.

### rseq
Restartable sequences (rseq) enable fast per-CPU operations in userspace with minimal kernel involvement. They are a performance feature for high-throughput runtimes and libraries.

### CPU hotplug
CPU hotplug allows CPUs to be dynamically brought online or taken offline. This is essential for power management, virtualization, and fault handling, and it touches nearly every core subsystem.

### pidfd
pidfds are file-descriptor-based process references that avoid PID reuse races. They provide a safer foundation for process management APIs.

### coredump
The coredump subsystem captures a process’s memory and state when it crashes. It is critical for post-mortem debugging and tightly integrated with memory management and signal handling.

## Memory Management

### folio
Folios represent groups of pages managed as a single unit. They simplify and optimize memory management by reducing per-page overhead and clarifying ownership rules.

### iomap
iomap is a generic block mapping layer used by modern filesystems. It unifies buffered and direct I/O paths and reduces duplicated filesystem code.

### writeback
Writeback controls how dirty memory pages are flushed to storage. It balances data integrity, latency, and throughput, and directly affects filesystem behavior under load.

### dma-mapping
The DMA mapping API handles memory visibility between devices and CPUs. It abstracts architecture-specific cache coherency and address translation rules.

### dmaengine
dmaengine provides a generic framework for offloading memory copies and similar operations to DMA hardware. It improves performance and reduces CPU usage.

## Virtual Filesystem (VFS) & Core FS Plumbing

### vfs
The VFS layer provides a unified interface for all filesystems. It defines core abstractions like files, dentries, and superblocks.

### vfs inode
Inodes represent filesystem objects in memory. VFS inode code manages lifecycle, caching, and synchronization across all filesystems.

### fs header
Filesystem headers define shared structures and interfaces between VFS and individual filesystems. Changes here ripple widely.

### superblock lock guard
This logic protects superblock state against concurrent access. It is part of ongoing efforts to harden filesystem locking.

### directory locking
Directory locking governs concurrent access to directory contents. It is crucial for correctness and performance under heavy filesystem activity.

### directory delegations
Delegations allow certain directory operations to be safely deferred or shared, improving scalability in networked and complex filesystems.

### fd prepare
File-descriptor preparation handles validation and setup before exposing descriptors to userspace. It is a subtle but security-sensitive path.

## Local Filesystems

### ext4
ext4 is the default Linux filesystem, balancing maturity, performance, and reliability.

### xfs
XFS is a high-performance filesystem optimized for large files and parallel workloads.

### btrfs
Btrfs is a copy-on-write filesystem with snapshots, checksums, and advanced volume management.

### f2fs
F2FS is designed for flash-based storage, optimizing wear leveling and write patterns.

### erofs
EROFS is a read-only filesystem optimized for compressed images.

### ntfs3
ntfs3 is the in-kernel NTFS implementation for compatibility with Windows filesystems.

### exfat
exFAT supports large removable media with broad cross-platform compatibility.

### minix
Minix is a simple filesystem mainly used for testing and educational purposes.

### hfs/hfsplus
These filesystems support Apple’s legacy disk formats.

### UBI and UBIFS
UBI and UBIFS manage raw flash devices, handling wear leveling and bad blocks.

## Network and Virtual Filesystems

### nfsd
The NFS server implementation exports filesystems over the network.

### NFS client
The NFS client allows Linux to mount remote NFS exports.

### smb client
The SMB client provides access to Windows-style network shares.

### smb server
The SMB server exports Linux filesystems to SMB clients.

### 9p
9p is a lightweight network filesystem used heavily by virtualization systems.

### fuse
FUSE allows filesystems to be implemented in userspace.

### overlayfs
OverlayFS layers filesystems to present a unified view.

### autofs
Autofs automatically mounts filesystems on demand.

## Virtualization & Isolation

### KVM
KVM provides hardware-assisted virtualization.

### VFIO
VFIO enables safe direct device access from userspace and virtual machines.

### iommufd
iommufd exposes IOMMU functionality through a file-descriptor-based API.

### iommu
The IOMMU controls device memory access and isolation.

### virtio
Virtio defines paravirtualized device interfaces for guests.

### hyperv
Hyper-V support integrates Linux with Microsoft’s hypervisor.

### namespace
Namespaces isolate global system resources between processes.

### UML
User Mode Linux runs the kernel as a userspace process.

## Architecture

### csky
C-SKY is a RISC architecture supported by the Linux kernel.

### turbostat
Turbostat reports CPU frequency, power, and idle state statistics.

## Device Drivers (General)

### input
Input drivers handle keyboards, mice, and similar devices.

### HID
HID supports USB and Bluetooth human interface devices.

### tty/serial
TTY and serial drivers provide terminal and serial port support.

### hwmon
Hwmon exposes hardware sensors to userspace.

### GNSS
GNSS drivers support satellite navigation devices.

### IPMI
IPMI provides out-of-band management for servers.

### soundwire
SoundWire is a digital audio interconnect.

### phy
PHY drivers manage physical layer devices.

### ata
ATA drivers support SATA and PATA storage devices.

### mtd
MTD handles raw flash memory devices.

### device mapper
Device Mapper provides logical block device abstractions.

### nvdimm
NVDIMM supports persistent memory devices.

### clk
The clock framework manages hardware clocks.

## Buses, Interconnects & Low-Level I/O

### USB/Thunderbolt
USB and Thunderbolt drivers handle external peripherals and high-speed I/O.

### compute express link (CXL)
CXL is a cache-coherent interconnect for accelerators and memory expansion.

### MSI
Message Signaled Interrupts replace legacy interrupt lines.

### ACPI
ACPI provides firmware-based hardware discovery and power management.

### devicetree
Device Tree describes hardware layout for non-ACPI systems.

## Networking & High-Performance I/O

### networking
The networking stack implements protocols, routing, and packet processing.

### rdma
RDMA enables low-latency, zero-copy networking.

### io_uring
io_uring provides a high-performance asynchronous I/O interface.

### block
The block layer manages storage I/O scheduling and submission.

### remoteproc
Remoteproc manages auxiliary processors on SoCs.

### rpmsg
Rpmsg provides messaging between CPUs.

### mailbox-adjacent logic
Mailbox frameworks enable simple inter-processor communication.

## IRQs, Timers & Timekeeping

### irq core
IRQ core manages interrupt registration and dispatch.

### irq driver
IRQ drivers handle hardware-specific interrupt controllers.

### core irq
Core IRQ logic coordinates interrupt handling.

### clocksource
Clocksources provide timekeeping primitives.

### timer core
Timer core schedules timed events.

## Observability, Performance & Debugging

### perf event
Perf events collect performance counters.

### perf tools
Perf tools expose profiling data to userspace.

## tools and testing

### Kbuild
Kbuild is the kernel build system.

### objtool
Objtool validates low-level object code.

### kselftest
Kselftest provides in-kernel test suites.

### kunit
KUnit is a unit testing framework for kernel code.

## random

### auxdisplay
Auxdisplay supports small auxiliary displays.

### random number generator
The RNG subsystem provides entropy and randomness.

### sysctl
Sysctl exposes kernel parameters at runtime.

### configfs
Configfs exposes kernel object configuration via a filesystem.


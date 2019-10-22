# monitor

## iostat

![iostat](C:\Users\SUN\Documents\git_mytest\mytest\iostat.PNG)

| 第一行  | 显示系统版本、主机名、当前日期                               |
| ------- | ------------------------------------------------------------ |
| avg-cpu | 总体cpu使用情况统计信息，对于多核cpu，这里为所有的cpu的平均值 |
| Device  | 各磁盘设备的IO统计信息                                       |

avg-cpu: 

| 选项    | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| %user   | CPU在用户态执行进程的时间百分比                              |
| %nice   | CPU在用户模式下，用于nice操作，所占用CPU总时间的百分比       |
| %system | CPU处在内核态执行进程的时间百分比                            |
| %iowait | CPU用于等待I/O操作占用CPU总时间的百分比                      |
| %steal  | 管理程序（hypervisor）为另一个虚拟进程提供服务而等待虚拟CPU的百分比 |
| %idle   | CPU空闲时间百分比                                            |

若 %iowait的值过高，表示硬盘存在I/O瓶颈

若 %idle 的值高但系统响应慢时，有可能是CPU等待分配内存，此时应加大内存容量 

若 %idle 的值持续低于1，则系统的CPU处理能力相对较低，表明系统中最需要解决的资源是 CPU



device 中各列参数含义：

| 选项       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| Device     |                                                              |
| tps        | 每秒向磁盘设备请求数据的次数，包括读、写请求，为rtps与wtps的和。出于效率考虑，每一次IO下发后并不是立即处理请求，而是将请求合并(merge)，这里tps指请求合并后的请求计数。 |
| Blk_read/s | Indicate the amount of data read from the device expressed in a number of blocks per second. Blocks are equivalent to sectors with kernels 2.4 and later and therefore have a size of 512 bytes. With older kernels, a block is of indeterminate size. |
| Blk_wrtn/s | Indicate the amount of data written to the device expressed in a number of blocks per second. |
| Blk_read   | 取样时间间隔内读扇区总数量                                   |
| Blk_wrtn   | 取样时间间隔内写扇区总数量                                   |

![动态查硬盘io](C:\Users\SUN\Documents\git_mytest\mytest\动态查硬盘io.PNG)

| 选项     | 说明                                                         |
| :------- | :----------------------------------------------------------- |
| rrqm/s   | 每秒对该设备的读请求被合并次数，文件系统会对读取同块(block)的请求进行合并 |
| wrqm/s   | 每秒对该设备的写请求被合并次数                               |
| r/s      | 每秒完成的读次数                                             |
| w/s      | 每秒完成的写次数                                             |
| rkB/s    | 每秒读数据量(kB为单位)                                       |
| wkB/s    | 每秒写数据量(kB为单位)                                       |
| avgrq-sz | 平均每次IO操作的数据量(扇区数为单位)                         |
| avgqu-sz | 平均等待处理的IO请求队列长度                                 |
| await    | 平均每次IO请求**等待时间**(包括等待时间和处理时间，毫秒为单位) |
| svctm    | 平均每次IO请求的**处理时间**(毫秒为单位)                     |
| %util    | 采用周期内用于IO操作的时间比率，即IO队列非空的时间比率（磁盘使用率） |
# Java锁机制面试题详解 (20道)

## 一、基础概念题 (1-5题)

### 1. 什么是Java中的锁？
**答案：** 锁是Java中用于控制多线程并发访问共享资源的机制。主要目的是保证线程安全，避免数据不一致问题。

```java
// 锁的基本使用
public class Counter {
    private int count = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized(lock) {
            count++;
        }
    }
}
```

### 2. synchronized关键字的作用是什么？
**答案：** synchronized是Java中最基本的同步机制，它可以修饰：
- **实例方法**：锁住当前实例对象
- **静态方法**：锁住当前类的Class对象
- **代码块**：锁住指定的对象

```java
// 三种使用方式
public class SyncExample {
    
    // 1. 实例方法
    public synchronized void instanceMethod() {
        // 锁住当前实例
    }
    
    // 2. 静态方法
    public static synchronized void staticMethod() {
        // 锁住Class对象
    }
    
    // 3. 同步代码块
    public void syncBlock() {
        synchronized(this) {
            // 锁住指定对象
        }
    }
}
```

### 3. 什么是重入锁(ReentrantLock)？
**答案：** ReentrantLock是JDK 5引入的显式锁，相比synchronized提供更灵活的锁定机制。

```java
// ReentrantLock使用
import java.util.concurrent.locks.ReentrantLock;

public class ReentrantLockExample {
    private final ReentrantLock lock = new ReentrantLock();
    private int count = 0;
    
    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }
    
    // 可重入性示例
    public void outer() {
        lock.lock();
        try {
            inner(); // 可以再次获取锁
        } finally {
            lock.unlock();
        }
    }
    
    public void inner() {
        lock.lock(); // 重入锁
        try {
            // ...
        } finally {
            lock.unlock();
        }
    }
}
```

### 4. synchronized和ReentrantLock的区别？
**答案：**

| 特性 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现方式 | JVM内置 | JDK代码实现 |
| 锁释放 | 自动释放 | 手动unlock() |
| 可中断 | 不可中断 | 可中断(lockInterruptibly) |
| 公平锁 | 不支持 | 支持(fair=true) |
| 条件变量 | 不支持 | 支持(Condition) |
| 性能 | JDK5之前更好 | JDK5之后更好 |

```java
// ReentrantLock高级特性
public class ReentrantLockFeatures {
    private final ReentrantLock lock = new ReentrantLock(true); // 公平锁
    private final Condition condition = lock.newCondition();
    
    public void await() throws InterruptedException {
        lock.lockInterruptibly(); // 可中断获取锁
        try {
            condition.await(); // 等待条件
        } finally {
            lock.unlock();
        }
    }
    
    public void signal() {
        lock.lock();
        try {
            condition.signal(); // 唤醒等待线程
        } finally {
            lock.unlock();
        }
    }
}
```

### 5. 什么是自旋锁(Spinlock)？
**答案：** 自旋锁是指线程在获取锁失败时，不会立即进入阻塞状态，而是在循环中不断尝试获取锁，直到成功或达到最大自旋次数。

```java
// 自旋锁实现
public class SpinLock {
    private final AtomicReference<Thread> owner = new AtomicReference<>();
    
    public void lock() {
        Thread current = Thread.currentThread();
        while (!owner.compareAndSet(null, current)) {
            // 自旋，可以加入Thread.yield()或Thread.sleep()
        }
    }
    
    public void unlock() {
        owner.set(null);
    }
}

// JVM中的自旋锁优化
// -XX:+UseSpinning 启用自旋锁
// -XX:PreBlockSpin 设置自旋次数(默认10次)
```

## 二、进阶概念题 (6-10题)

### 6. 什么是AQS(AbstractQueuedSynchronizer)？
**答案：** AQS是Java并发包的核心基础类，用于构建锁和其他同步器。它维护了一个FIFO队列和状态变量。

```java
// AQS核心原理
public abstract class AQS {
    // 状态变量
    private volatile int state;
    
    // 等待队列
    private transient volatile Node head;
    private transient volatile Node tail;
    
    // 获取锁(模板方法)
    public final void acquire(int arg) {
        if (!tryAcquire(arg) && acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt();
    }
    
    // 释放锁(模板方法)
    public final boolean release(int arg) {
        if (tryRelease(arg)) {
            Node h = head;
            if (h != null && h.waitStatus != 0)
                unparkSuccessor(h);
            return true;
        }
        return false;
    }
}

// ReentrantLock基于AQS实现
class NonfairSync extends Sync {
    protected final boolean tryAcquire(int acquires) {
        return nonfairTryAcquire(acquires);
    }
}
```

### 7. 什么是读写锁(ReadWriteLock)？
**答案：** 读写锁允许多个读线程同时访问，但在写线程访问时独占。提高了并发性能。

```java
// 读写锁使用
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReadWriteLockExample {
    private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final Map<String, String> data = new HashMap<>();
    
    public String get(String key) {
        rwLock.readLock().lock();
        try {
            return data.get(key);
        } finally {
            rwLock.readLock().unlock();
        }
    }
    
    public void put(String key, String value) {
        rwLock.writeLock().lock();
        try {
            data.put(key, value);
        } finally {
            rwLock.writeLock().unlock();
        }
    }
    
    public void clear() {
        rwLock.writeLock().lock();
        try {
            data.clear();
        } finally {
            rwLock.writeLock().unlock();
        }
    }
}
```

### 8. 什么是分段锁(Segment Lock)？
**答案：** 分段锁是将数据分成多个段，每个段独立加锁，提高并发性能。ConcurrentHashMap就是使用分段锁思想。

```java
// 分段锁实现思想
public class SegmentLock<K, V> {
    private final int segmentCount;
    private final Object[] locks;
    private final Map<K, V>[] segments;
    
    @SuppressWarnings("unchecked")
    public SegmentLock(int segmentCount) {
        this.segmentCount = segmentCount;
        this.locks = new Object[segmentCount];
        this.segments = new HashMap[segmentCount];
        
        for (int i = 0; i < segmentCount; i++) {
            locks[i] = new Object();
            segments[i] = new HashMap<>();
        }
    }
    
    private int getSegmentIndex(K key) {
        return Math.abs(key.hashCode()) % segmentCount;
    }
    
    public V get(K key) {
        int index = getSegmentIndex(key);
        synchronized (locks[index]) {
            return segments[index].get(key);
        }
    }
    
    public void put(K key, V value) {
        int index = getSegmentIndex(key);
        synchronized (locks[index]) {
            segments[index].put(key, value);
        }
    }
}
```

### 9. 什么是悲观锁和乐观锁？
**答案：** 
- **悲观锁**：认为并发冲突概率高，先加锁再操作
- **乐观锁**：认为并发冲突概率低，先操作再检查冲突

```java
// 悲观锁实现
public class PessimisticLock {
    private final Map<String, Integer> data = new HashMap<>();
    private final Object lock = new Object();
    
    public void increment(String key) {
        synchronized(lock) {
            Integer value = data.get(key);
            if (value == null) {
                data.put(key, 1);
            } else {
                data.put(key, value + 1);
            }
        }
    }
}

// 乐观锁实现(版本号机制)
public class OptimisticLock {
    private static class Data {
        private String key;
        private String value;
        private int version; // 版本号
        
        // getters and setters
    }
    
    private final Map<String, Data> data = new HashMap<>();
    
    public void update(String key, String newValue) {
        Data existing = data.get(key);
        if (existing != null) {
            // 检查版本号
            if (existing.getVersion() != getCurrentVersion(key)) {
                throw new OptimisticLockException("数据已被修改");
            }
            existing.setValue(newValue);
            existing.setVersion(existing.getVersion() + 1);
        }
    }
}

// CAS实现乐观锁
public class CasOptimisticLock {
    private final AtomicStampedReference<String> value = 
        new AtomicStampedReference<>("", 0);
    
    public void update(String newValue) {
        int stamp = value.getStamp();
        while (!value.compareAndSet(value.getReference(), newValue, stamp, stamp + 1)) {
            stamp = value.getStamp();
        }
    }
}
```

### 10. 什么是死锁？如何避免？
**答案：** 死锁是指两个或多个线程互相等待对方持有的锁，导致所有线程都无法继续执行。

```java
// 死锁示例
public class DeadLockExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    public void method1() {
        synchronized(lock1) {
            synchronized(lock2) {
                // 执行操作
            }
        }
    }
    
    public void method2() {
        synchronized(lock2) {
            synchronized(lock1) {
                // 执行操作
            }
        }
    }
}

// 避免死锁的策略
public class DeadLockPrevention {
    // 1. 锁顺序化
    public void method1() {
        Object first = getFirstLock();
        Object second = getSecondLock();
        synchronized(first) {
            synchronized(second) {
                // 执行操作
            }
        }
    }
    
    public void method2() {
        Object first = getFirstLock(); // 相同的获取顺序
        Object second = getSecondLock();
        synchronized(first) {
            synchronized(second) {
                // 执行操作
            }
        }
    }
    
    // 2. 使用超时锁
    private final ReentrantLock lock1 = new ReentrantLock();
    private final ReentrantLock lock2 = new ReentrantLock();
    
    public boolean tryMethod() {
        try {
            if (lock1.tryLock(500, TimeUnit.MILLISECONDS)) {
                try {
                    if (lock2.tryLock(500, TimeUnit.MILLISECONDS)) {
                        try {
                            // 执行操作
                            return true;
                        } finally {
                            lock2.unlock();
                        }
                    }
                } finally {
                    lock1.unlock();
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return false;
    }
}
```

## 三、JUC锁机制 (11-15题)

### 11. 什么是StampedLock？
**答案：** StampedLock是JDK 8引入的读写锁优化版本，提供了三种访问模式：读、写、乐观读。

```java
// StampedLock使用
import java.util.concurrent.locks.StampedLock;

public class StampedLockExample {
    private final StampedLock lock = new StampedLock();
    private double x, y;
    
    // 写锁
    public void move(double deltaX, double deltaY) {
        long stamp = lock.writeLock();
        try {
            x += deltaX;
            y += deltaY;
        } finally {
            lock.unlockWrite(stamp);
        }
    }
    
    // 悲观读锁
    public double distanceFromOrigin() {
        long stamp = lock.readLock();
        try {
            return Math.sqrt(x * x + y * y);
        } finally {
            lock.unlockRead(stamp);
        }
    }
    
    // 乐观读锁
    public double distanceFromOriginOptimistic() {
        long stamp = lock.tryOptimisticRead();
        double currentX = x;
        double currentY = y;
        
        if (!lock.validate(stamp)) {
            stamp = lock.readLock();
            try {
                currentX = x;
                currentY = y;
            } finally {
                lock.unlockRead(stamp);
            }
        }
        return Math.sqrt(currentX * currentX + currentY * currentY);
    }
    
    // 锁转换
    public void moveIfAtOrigin(double newX, double newY) {
        long stamp = lock.readLock();
        try {
            while (x == 0 && y == 0) {
                long ws = lock.tryConvertToWriteLock(stamp);
                if (ws != 0L) {
                    stamp = ws;
                    x = newX;
                    y = newY;
                    break;
                } else {
                    lock.unlockRead(stamp);
                    stamp = lock.writeLock();
                }
            }
        } finally {
            lock.unlock(stamp);
        }
    }
}
```

### 12. 什么是Semaphore？
**答案：** Semaphore（信号量）是用于控制同时访问特定资源的线程数量，基于AQS实现。

```java
// Semaphore使用
import java.util.concurrent.Semaphore;

public class SemaphoreExample {
    private final Semaphore semaphore = new Semaphore(3); // 允许3个线程同时访问
    
    public void accessResource() throws InterruptedException {
        semaphore.acquire();
        try {
            // 访问共享资源
            System.out.println("Thread " + Thread.currentThread().getName() + " accessing resource");
            Thread.sleep(1000);
        } finally {
            semaphore.release();
        }
    }
    
    // 带超时的获取
    public boolean tryAccessResource(long timeout, TimeUnit unit) throws InterruptedException {
        if (semaphore.tryAcquire(timeout, unit)) {
            try {
                // 访问资源
                return true;
            } finally {
                semaphore.release();
            }
        }
        return false;
    }
    
    // 获取多个许可
    public void bulkAccess() throws InterruptedException {
        semaphore.acquire(5); // 获取5个许可
        try {
            // 执行需要大量资源的操作
        } finally {
            semaphore.release(5);
        }
    }
}
```

### 13. 什么是CountDownLatch？
**答案：** CountDownLatch是一个同步工具，允许一个或多个线程等待其他线程完成操作。

```java
// CountDownLatch使用
import java.util.concurrent.CountDownLatch;

public class CountDownLatchExample {
    private final CountDownLatch startLatch = new CountDownLatch(1);
    private final CountDownLatch completeLatch = new CountDownLatch(5);
    
    public void executeTasks() throws InterruptedException {
        // 启动5个工作线程
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            new Thread(() -> {
                try {
                    startLatch.await(); // 等待启动信号
                    System.out.println("Task " + taskId + " started");
                    Thread.sleep(1000);
                    System.out.println("Task " + taskId + " completed");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    completeLatch.countDown(); // 任务完成
                }
            }).start();
        }
        
        Thread.sleep(500);
        startLatch.countDown(); // 发送启动信号
        
        completeLatch.await(); // 等待所有任务完成
        System.out.println("All tasks completed");
    }
}
```

### 14. 什么是CyclicBarrier？
**答案：** CyclicBarrier是一个同步工具，允许多个线程相互等待，到达一个屏障点后再一起继续执行。

```java
// CyclicBarrier使用
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierExample {
    private final CyclicBarrier barrier = new CyclicBarrier(3, () -> {
        System.out.println("All parties have arrived at the barrier");
    });
    
    public void run() {
        for (int i = 0; i < 3; i++) {
            final int partyId = i;
            new Thread(() -> {
                try {
                    System.out.println("Party " + partyId + " is approaching the barrier");
                    Thread.sleep(1000);
                    System.out.println("Party " + partyId + " has arrived at the barrier");
                    barrier.await();
                    System.out.println("Party " + partyId + " has passed the barrier");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
    
    // 带超时的等待
    public void runWithTimeout() {
        try {
            barrier.await(2, TimeUnit.SECONDS);
        } catch (TimeoutException e) {
            System.out.println("Timeout waiting for barrier");
        }
    }
}
```

### 15. 什么是Phaser？
**答案：** Phaser是JDK 7引入的更灵活的同步工具，可以动态注册和注销参与方，支持多阶段同步。

```java
// Phaser使用
import java.util.concurrent.Phaser;

public class PhaserExample {
    private final Phaser phaser = new Phaser(1); // 注册1个参与方(主线程)
    
    public void executePhases() {
        // 启动3个工作线程
        for (int i = 0; i < 3; i++) {
            final int phaseId = i;
            phaser.register(); // 注册参与方
            new Thread(() -> {
                try {
                    // 第一阶段
                    System.out.println("Phase 1 - Thread " + phaseId);
                    phaser.arriveAndAwaitAdvance(); // 到达并等待其他线程
                    
                    // 第二阶段
                    System.out.println("Phase 2 - Thread " + phaseId);
                    phaser.arriveAndAwaitAdvance();
                    
                    // 第三阶段
                    System.out.println("Phase 3 - Thread " + phaseId);
                    phaser.arriveAndDeregister(); // 到达并注销
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();
        }
        
        // 主线程也参与
        System.out.println("Phase 1 - Main thread");
        phaser.arriveAndAwaitAdvance();
        
        System.out.println("Phase 2 - Main thread");
        phaser.arriveAndAwaitAdvance();
        
        System.out.println("Phase 3 - Main thread");
        phaser.arriveAndDeregister();
    }
}
```

## 四、高级特性和最佳实践 (16-20题)

### 16. 什么是锁消除(Lock Elision)？
**答案：** 锁消除是JVM的优化技术，通过逃逸分析判断对象不会逃逸出方法或线程，从而消除不必要的同步。

```java
// 锁消除示例
public class LockElision {
    
    // 方法内局部变量，可以被锁消除
    public void method() {
        StringBuilder sb = new StringBuilder();
        synchronized(sb) { // sb不会逃逸，锁可能被消除
            sb.append("hello");
        }
    }
    
    // 逃逸分析失败，无法锁消除
    public void method2(StringBuilder sb) {
        synchronized(sb) { // sb可能逃逸，无法消除
            sb.append("hello");
        }
    }
    
    // JVM参数
    // -XX:+DoEscapeAnalysis 启用逃逸分析(默认开启)
    // -XX:+EliminateLocks 启用锁消除(默认开启)
}
```

### 17. 什么是锁粗化(Lock Coarsening)？
**答案：** 锁粗化是JVM的优化技术，将多个连续的锁操作合并为一个更大的锁范围，减少锁获取和释放的开销。

```java
// 锁粗化示例
public class LockCoarsening {
    
    // 可能被粗化的代码
    public void method() {
        synchronized(this) {
            // 操作1
        }
        synchronized(this) {
            // 操作2
        }
        synchronized(this) {
            // 操作3
        }
    }
    
    // JVM可能优化为
    public void methodOptimized() {
        synchronized(this) {
            // 操作1
            // 操作2
            // 操作3
        }
    }
}
```

### 18. 如何诊断和解决锁竞争问题？
**答案：** 使用工具诊断锁竞争，然后采用相应策略解决。

```java
// 锁竞争诊断
public class LockContentionDiagnosis {
    
    // 1. JStack查看线程状态
    public void diagnoseWithJstack() {
        // 执行jstack命令
        // jstack <pid> > thread_dump.txt
        // 查看BLOCKED状态的线程
    }
    
    // 2. JVisualVM监控
    public void diagnoseWithVisualVM() {
        // 使用JVisualVM监控锁竞争
        // 查看线程状态和锁信息
    }
    
    // 3. Java Flight Recorder
    public void diagnoseWithJFR() {
        // 使用JFR记录锁事件
        // -XX:+UnlockCommercialFeatures -XX:+FlightRecorder
    }
    
    // 解决方案
    public void solutions() {
        // 1. 减小锁粒度
        // 2. 使用读写锁
        // 3. 使用并发容器
        // 4. 使用CAS操作
        // 5. 锁分离
    }
}
```

### 19. 什么是无锁编程？
**答案：** 无锁编程是指不使用传统锁机制来实现线程安全的编程技术，主要依赖CAS操作和原子变量。

```java
// 无锁编程示例
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

public class LockFreeProgramming {
    
    // 1. 原子变量
    private final AtomicInteger counter = new AtomicInteger(0);
    
    public void increment() {
        int oldValue;
        int newValue;
        do {
            oldValue = counter.get();
            newValue = oldValue + 1;
        } while (!counter.compareAndSet(oldValue, newValue));
    }
    
    // 2. 无锁栈
    private static class Node<T> {
        final T item;
        Node<T> next;
        
        Node(T item) {
            this.item = item;
        }
    }
    
    private final AtomicReference<Node<Integer>> top = new AtomicReference<>();
    
    public void push(Integer item) {
        Node<Integer> newHead = new Node<>(item);
        Node<Integer> oldHead;
        do {
            oldHead = top.get();
            newHead.next = oldHead;
        } while (!top.compareAndSet(oldHead, newHead));
    }
    
    public Integer pop() {
        Node<Integer> oldHead;
        Node<Integer> newHead;
        do {
            oldHead = top.get();
            if (oldHead == null) {
                return null;
            }
            newHead = oldHead.next;
        } while (!top.compareAndSet(oldHead, newHead));
        return oldHead.item;
    }
}
```

### 20. 锁的最佳实践是什么？
**答案：** 遵循最佳实践可以写出更高效、更安全的并发代码。

```java
// 锁最佳实践
public class LockBestPractices {
    
    // 1. 尽量使用局部变量锁
    public void bestPractice1() {
        final Object lock = new Object(); // 局部变量锁
        synchronized(lock) {
            // ...
        }
    }
    
    // 2. 优先使用java.util.concurrent包
    public void bestPractice2() {
        // 使用并发容器
        Map<String, String> map = new ConcurrentHashMap<>();
        
        // 使用原子变量
        AtomicInteger counter = new AtomicInteger(0);
        
        // 使用锁工具类
        ReentrantLock lock = new ReentrantLock();
    }
    
    // 3. 减小锁范围
    public void bestPractice3() {
        // 不好的做法：锁住整个方法
        public synchronized void badMethod() {
            // 耗时操作
            // 访问数据库
            // 网络IO
        }
        
        // 好的做法：只锁必要的部分
        public void goodMethod() {
            // 不需要锁的操作
            synchronized(this) {
                // 只需要锁的操作
            }
            // 不需要锁的操作
        }
    }
    
    // 4. 使用try-finally确保锁释放
    public void bestPractice4() {
        ReentrantLock lock = new ReentrantLock();
        lock.lock();
        try {
            // 操作共享资源
        } finally {
            lock.unlock(); // 确保锁被释放
        }
    }
    
    // 5. 避免在锁内调用外部方法
    public void bestPractice5() {
        // 不好的做法
        synchronized(this) {
            externalMethod(); // 可能死锁
        }
        
        // 好的做法
        Object result = externalMethod(); // 先调用
        synchronized(this) {
            // 使用结果
        }
    }
    
    // 6. 使用适当的锁策略
    public void bestPractice6() {
        // 读多写少：使用读写锁
        ReadWriteLock rwLock = new ReentrantReadWriteLock();
        
        // 写多读少：使用互斥锁
        Lock writeLock = new ReentrantLock();
        
        // 高并发：使用无锁算法
        AtomicInteger atomicCounter = new AtomicInteger();
    }
}
```

## 五、性能调优参数

### JVM锁调优参数
```bash
# 锁优化参数
-XX:+UseBiasedLocking           # 启用偏向锁(默认开启)
-XX:+UseSpinning                # 启用自旋锁(默认开启)
-XX:PreBlockSpin=10             # 设置自旋次数
-XX:+EliminateLocks             # 启用锁消除(默认开启)
-XX:+DoEscapeAnalysis           # 启用逃逸分析(默认开启)

# 监控参数
-XX:+PrintGCDetails             # 打印GC详情
-XX:+PrintConcurrentLocks       # 打印并发锁信息
```

---

**更新时间：** 2026-03-14
**适用级别：** 高级开发工程师
**面试重点：** 锁机制原理、并发编程、性能优化
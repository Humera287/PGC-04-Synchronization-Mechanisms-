# PGC-04: Synchronization Mechanisms in Parallel Programs

> **Course:** Parallel and GPU Computing (PGC)  
> **Author:** Humera  
> **USN:** `01FE24BCI114`   
> **Repository:** `PGC-04-Synchronization-Mechanisms`

---

## Table of Contents

- [1. Aim and Objectives](#1-aim-and-objectives)
- [2. Understanding Synchronization](#2-understanding-synchronization)
  - [2.1 Race Condition](#21-race-condition)
  - [2.2 Why Counter Increment Fails](#22-why-counter-increment-fails)
  - [2.3 Synchronization Techniques](#23-synchronization-techniques)
- [3. Setup and Environment](#3-setup-and-environment)
- [4. Programs and Execution](#4-programs-and-execution)
  - [Program 1: Race Condition](#program-1-race-condition)
  - [Program 2: Critical Section](#program-2-critical-section)
  - [Program 3: Atomic Operation](#program-3-atomic-operation)
  - [Program 4: Barrier Synchronization](#program-4-barrier-synchronization)
  - [Program 5: POSIX Semaphore](#program-5-posix-semaphore)
  - [Program 6: Synchronization Benchmark](#program-6-synchronization-benchmark)
- [5. Performance Analysis](#5-performance-analysis)
  - [5.1 Race Condition Data Loss](#51-race-condition-data-loss)
  - [5.2 Execution Time Comparison](#52-execution-time-comparison)
  - [5.3 Atomic Operation vs Critical Section](#53-atomic-operation-vs-critical-section)
  - [5.4 Critical Section vs Lock](#54-critical-section-vs-lock)
  - [5.5 Performance Conclusion](#55-performance-conclusion)

---

## 1. Aim and Objectives

The aim of this experiment is to understand synchronization mechanisms in parallel programs and study how multiple threads safely access shared data.

### Objectives

1. Understand race conditions in multithreaded programs.
2. Implement synchronization using critical sections, atomic operations, barriers, and semaphores.
3. Compare the correctness of synchronized and unsynchronized programs.
4. Measure execution time for different synchronization techniques.
5. Analyze performance with 1, 2, 4, and 8 threads.

---

## 2. Understanding Synchronization

### 2.1 Race Condition

A race condition occurs when multiple threads access and modify the same shared variable simultaneously, producing an unpredictable result.

For example, suppose the counter value is 100.

```text
Thread 1 reads counter = 100
Thread 2 reads counter = 100
Thread 1 increments and writes 101
Thread 2 increments and writes 101

Expected counter = 102
Actual counter   = 101
```

One update is lost because both threads read the same original value.

### 2.2 Why Counter Increment Fails

The statement `counter++` involves three logical steps:

1. Read the current counter value.
2. Increment the value.
3. Write the updated value.

When multiple threads execute these steps simultaneously, their operations may overlap, resulting in lost updates.

Synchronization mechanisms prevent conflicting updates.

### 2.3 Synchronization Techniques

**1. No Synchronization**

Threads access the shared variable without protection. This can produce incorrect results.

**2. Critical Section**

The `#pragma omp critical` directive allows only one thread at a time to execute the protected block.

**3. Atomic Operation**

The `#pragma omp atomic` directive protects a supported shared-variable operation.

**4. Barrier**

The `#pragma omp barrier` directive makes threads wait until all threads in the team reach the same point.

**5. POSIX Semaphore**

`sem_wait()` and `sem_post()` control access to a shared resource.

**6. OpenMP Lock**

An OpenMP lock explicitly controls entry into and exit from a protected section.

---

## 3. Setup and Environment

### System Configuration

| Component | Details |
|---|---|
| Operating System | Ubuntu Linux |
| Virtualization Platform | VMware Workstation |
| Compiler | GCC 15.2.0 |
| Parallel Programming Support | OpenMP |
| Thread Library | POSIX Threads |
| Number of Threads Tested | 1, 2, 4, 8 |
| Number of Increments | 10,000,000 |

### Step 1: Update Package Information

Command:

```bash
sudo apt update
```

**Observation:** Package information was updated successfully.

### Step 2: Install Build Tools

Command:

```bash
sudo apt install build-essential -y
```

**Observation:** The `build-essential` package was already installed.

### Step 3: Verify GCC

Command:

```bash
gcc --version
```

**Output:**

```text
gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0
Copyright (C) 2025 Free Software Foundation, Inc.
```

### Step 4: Verify OpenMP Support

Command:

```bash
echo '#include <omp.h>' | gcc -E -fopenmp -xc - > /dev/null && echo OpenMP OK
```

**Output:**

```text
OpenMP OK
```

**Result:** GCC and OpenMP were successfully verified in the Ubuntu VMware environment.

---

## 4. Programs and Execution

### Program 1: Race Condition

**File:** `race.c`

**Objective:** Demonstrate the effect of updating a shared counter without synchronization.

#### Program

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    long counter = 0;

    #pragma omp parallel for
    for (long i = 0; i < 10000000; i++) {
        counter++;
    }

    printf("Counter=%ld\n", counter);

    return 0;
}
```

#### Compilation and Execution

```bash
gcc race.c -fopenmp -o race
./race
```

#### Actual Output

```text
Counter=1447683
```

#### Observation

The expected counter value was `10000000`, but the actual result was `1447683`.

This happened because multiple threads updated the shared counter without synchronization, causing lost updates.

The result demonstrates a race condition.

---

### Program 2: Critical Section

**File:** `critical.c`

**Objective:** Protect the shared counter using an OpenMP critical section.

#### Program

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    long counter = 0;

    #pragma omp parallel for
    for (long i = 0; i < 10000000; i++) {
        #pragma omp critical
        {
            counter++;
        }
    }

    printf("Counter=%ld\n", counter);

    return 0;
}
```

#### Compilation and Execution

```bash
gcc critical.c -fopenmp -o critical
./critical
```

#### Actual Output

```text
Counter=10000000
```

#### Observation

The critical section ensured that only one thread incremented the counter at a time.

The final count was correct. However, threads had to wait for access to the critical section, which increased execution time in the benchmark.

---

### Program 3: Atomic Operation

**File:** `atomic.c`

**Objective:** Use an OpenMP atomic directive to protect the counter increment.

#### Program

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    long counter = 0;

    #pragma omp parallel for
    for (long i = 0; i < 10000000; i++) {
        #pragma omp atomic
        counter++;
    }

    printf("Counter=%ld\n", counter);

    return 0;
}
```

#### Compilation and Execution

```bash
gcc atomic.c -fopenmp -o atomic
./atomic
```

#### Actual Output

```text
Counter=10000000
```

#### Observation

The atomic directive protected the shared counter increment and produced the correct final count.

Atomic operations performed better than critical sections and locks in the multithreaded benchmark tests.

---

### Program 4: Barrier Synchronization

**File:** `barrier.c`

**Objective:** Ensure that all threads reach a synchronization point before proceeding.

#### Program

```c
#include <stdio.h>
#include <omp.h>

int main(void) {
    #pragma omp parallel
    {
        printf("Thread %d before barrier\n",
               omp_get_thread_num());

        #pragma omp barrier

        printf("Thread %d after barrier\n",
               omp_get_thread_num());
    }

    return 0;
}
```

#### Compilation and Execution

```bash
gcc barrier.c -fopenmp -o barrier
./barrier
```

#### Actual Output

The terminal displayed messages similar to the following:

```text
Thread 0 before barrier
Thread 2 before barrier
Thread 3 before barrier
Thread 4 before barrier
Thread 1 before barrier
Thread 6 before barrier
Thread 5 before barrier
Thread 7 before barrier
Thread 0 after barrier
Thread 2 after barrier
Thread 4 after barrier
Thread 3 after barrier
Thread 5 after barrier
Thread 1 after barrier
Thread 7 after barrier
Thread 6 after barrier
```

**Note:** The exact order of thread messages may vary between executions.

#### Observation

All threads reached the barrier before any thread continued past it.

The program demonstrated how a barrier coordinates the execution of multiple threads.

---

### Program 5: POSIX Semaphore

**File:** `semaphore.c`

**Objective:** Protect a shared counter using a binary semaphore.

Two threads increment the counter 100,000 times each.

**Expected final count:** `200000`

#### Program

```c
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t semaphore;
int counter = 0;

void *work(void *arg) {
    for (int i = 0; i < 100000; i++) {
        sem_wait(&semaphore);

        counter++;

        sem_post(&semaphore);
    }

    return NULL;
}

int main(void) {
    pthread_t t1, t2;

    sem_init(&semaphore, 0, 1);

    pthread_create(&t1, NULL, work, NULL);
    pthread_create(&t2, NULL, work, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Counter=%d\n", counter);

    sem_destroy(&semaphore);

    return 0;
}
```

#### Compilation and Execution

```bash
gcc semaphore.c -pthread -o semaphore
./semaphore
```

#### Actual Output

```text
Counter=200000
```

#### Observation

The semaphore allowed only one thread at a time to enter the protected section.

- `sem_wait()` acquires the semaphore.
- `sem_post()` releases the semaphore.
- `pthread_join()` waits for the threads to finish.

The final count was correct.

---

### Program 6: Synchronization Benchmark

**File:** `compare_sync.c`

**Objective:** Compare the execution time and correctness of different synchronization mechanisms.

The benchmark tested:

- No synchronization
- Critical section
- Atomic operation
- OpenMP lock

#### Test Configuration

| Parameter | Value |
|---|---|
| Total increments | 10,000,000 |
| Thread counts | 1, 2, 4, 8 |
| Synchronization methods | None, Critical, Atomic, Lock |
| Measurements | Final count, correctness, execution time |

#### Compilation and Execution

```bash
gcc compare_sync.c -fopenmp -o compare_sync
./compare_sync
```

#### Actual Benchmark Output

```text
Comparing synchronization mechanisms for 10000000 shared increments

Mechanism | Threads | Final Count | Correctness | Time (s)

None      |    1    | 10000000   | Correct     | 0.0062
Critical  |    1    | 10000000   | Correct     | 0.0899
Atomic    |    1    | 10000000   | Correct     | 0.0532
Lock      |    1    | 10000000   | Correct     | 0.0894

None      |    2    | 6525906    | INCORRECT   | 0.0065
Critical  |    2    | 10000000   | Correct     | 0.3084
Atomic    |    2    | 10000000   | Correct     | 0.1268
Lock      |    2    | 10000000   | Correct     | 0.3643

None      |    4    | 3276185    | INCORRECT   | 0.0075
Critical  |    4    | 10000000   | Correct     | 0.6648
Atomic    |    4    | 10000000   | Correct     | 0.1226
Lock      |    4    | 10000000   | Correct     | 0.5535

None      |    8    | 1458522    | INCORRECT   | 0.0085
Critical  |    8    | 10000000   | Correct     | 1.0195
Atomic    |    8    | 10000000   | Correct     | 0.1184
Lock      |    8    | 10000000   | Correct     | 0.9216

Expected correct final count = 10000000
```

#### Benchmark Results Table

| Mechanism | Threads | Final Count | Correctness | Time (seconds) |
|---|---:|---:|---|---:|
| None | 1 | 10,000,000 | Correct | 0.0062 |
| Critical | 1 | 10,000,000 | Correct | 0.0899 |
| Atomic | 1 | 10,000,000 | Correct | 0.0532 |
| Lock | 1 | 10,000,000 | Correct | 0.0894 |
| None | 2 | 6,525,906 | Incorrect | 0.0065 |
| Critical | 2 | 10,000,000 | Correct | 0.3084 |
| Atomic | 2 | 10,000,000 | Correct | 0.1268 |
| Lock | 2 | 10,000,000 | Correct | 0.3643 |
| None | 4 | 3,276,185 | Incorrect | 0.0075 |
| Critical | 4 | 10,000,000 | Correct | 0.6648 |
| Atomic | 4 | 10,000,000 | Correct | 0.1226 |
| Lock | 4 | 10,000,000 | Correct | 0.5535 |
| None | 8 | 1,458,522 | Incorrect | 0.0085 |
| Critical | 8 | 10,000,000 | Correct | 1.0195 |
| Atomic | 8 | 10,000,000 | Correct | 0.1184 |
| Lock | 8 | 10,000,000 | Correct | 0.9216 |

#### Observation

1. The unsynchronized version was the fastest but produced incorrect results when multiple threads were used.
2. Critical sections produced correct results but became slower as the number of threads increased.
3. Atomic operations produced correct results and performed better than critical sections and locks in the multithreaded tests.
4. Locks produced correct results but introduced waiting overhead.
5. The atomic method achieved its lowest measured execution time at 8 threads in this benchmark.

---

## 5. Performance Analysis

### 5.1 Race Condition Data Loss

The percentage of lost updates can be calculated using the following formula:

```text
Data Loss (%) = ((Expected Count - Actual Count) / Expected Count) × 100
```

**Expected Count:** `10,000,000`

Using the actual benchmark outputs:

| Threads | Actual Count | Lost Updates | Data Loss |
|:---:|---:|---:|---:|
| 1 | 10,000,000 | 0 | 0% |
| 2 | 6,525,906 | 3,474,094 | 34.74% |
| 4 | 3,276,185 | 6,723,815 | 67.24% |
| 8 | 1,458,522 | 8,541,478 | 85.41% |

**Analysis:** Data loss increased as the number of threads increased in this particular run.

### 5.2 Execution Time Comparison

The following table compares the execution times of different synchronization methods.

| Threads | None (s) | Critical (s) | Atomic (s) | Lock (s) |
|:---:|---:|---:|---:|---:|
| 1 | 0.0062 | 0.0899 | 0.0532 | 0.0894 |
| 2 | 0.0065 | 0.3084 | 0.1268 | 0.3643 |
| 4 | 0.0075 | 0.6648 | 0.1226 | 0.5535 |
| 8 | 0.0085 | 1.0195 | 0.1184 | 0.9216 |

**Analysis:**

- **None:** Had the lowest execution time but produced incorrect results with multiple threads.
- **Critical:** Execution time increased from 0.0899 seconds with one thread to 1.0195 seconds with eight threads.
- **Atomic:** Execution time was 0.1184 seconds with eight threads, outperforming critical sections and locks in this test.
- **Lock:** Execution time increased as threads competed for access to the shared counter.

### 5.3 Atomic Operation vs Critical Section

At eight threads:

```text
Critical execution time = 1.0195 seconds
Atomic execution time   = 0.1184 seconds
```

The speed ratio is calculated as follows:

```text
Speed Ratio = Critical Time / Atomic Time

            = 1.0195 / 0.1184

            ≈ 8.61
```

**Result:** Atomic operations were approximately **8.61 times faster** than critical sections in the eight-thread benchmark.

This result applies to the measured execution and may vary on other systems.

### 5.4 Critical Section vs Lock

At eight threads:

```text
Critical execution time = 1.0195 seconds
Lock execution time     = 0.9216 seconds
```

The lock was faster than the critical section in this particular measurement, although both methods produced correct results.

### 5.5 Performance Conclusion

The experiment demonstrates that the fastest method is not always the most reliable.

The unsynchronized version executed quickly because it did not protect the shared counter, but it lost updates. Among the correct methods in this benchmark, the atomic operation provided the best execution time for the multithreaded tests.

## 6. Comparison Table

| Mechanism | Correctness | Main Advantage | Main Limitation |
|---|---|---|---|
| No Synchronization | Incorrect with multiple threads in this test | Lowest execution time | Race conditions and lost updates |
| Critical Section | Correct | Protects a block of code | High waiting overhead |
| Atomic Operation | Correct | Efficient for simple shared updates | Intended for supported atomic operations |
| OpenMP Lock | Correct | Explicit lock management | Lock contention |
| Barrier | Coordinates threads | Synchronizes execution phases | Threads may have to wait |
| POSIX Semaphore | Correct | Controls access to shared resources | Requires correct semaphore handling |

---

## 7. Compilation Commands

Run these commands from the directory containing the C source files.

### Race Condition

```bash
gcc race.c -fopenmp -o race
./race
```

### Critical Section
```bash
gcc critical.c -fopenmp -o critical
./critical
```

### Atomic Operation
```bash
gcc atomic.c -fopenmp -o atomic
./atomic
```

### Barrier
```bash
gcc barrier.c -fopenmp -o barrier
./barrier
```

### POSIX Semaphore
```bash
gcc semaphore.c -pthread -o semaphore
./semaphore
```

### Synchronization Comparison
```bash
gcc compare_sync.c -fopenmp -o compare_sync
./compare_sync
```

## 8. Execution Steps (Terminal)

| Step | Command | Purpose |
|---|---|---|
| 1 | `sudo apt update && sudo apt install build-essential -y` | Install GCC, Make, and the OpenMP runtime |
| 2 | `nano race.c` (repeat for each `.c` file) | Create and paste each program's source code |
| 3 | `gcc race.c -fopenmp -o race` | Compile the race-condition program |
| 4 | `gcc critical.c -fopenmp -o critical` | Compile the critical-section program |
| 5 | `gcc atomic.c -fopenmp -o atomic` | Compile the atomic-operation program |
| 6 | `gcc barrier.c -fopenmp -o barrier` | Compile the barrier program |
| 7 | `gcc semaphore.c -pthread -o semaphore` | Compile the semaphore program |
| 8 | `gcc compare_sync.c -fopenmp -o compare_sync` | Compile the comparison/benchmark program |
| 9 | `OMP_NUM_THREADS=4 ./atomic` | Run a program with a chosen number of threads |
| 10 | `./compare_sync` | Run the comparison across 1, 2, 4, and 8 threads and record timings |

You can also set the thread count using an environment variable before running an OpenMP program:

```bash
export OMP_NUM_THREADS=8
./critical
```

### 8.1 Installation and Basic Programs

<img width="877" height="525" alt="01_Installation_and_Basic_Programs" src="https://github.com/user-attachments/assets/1fc7a749-27ef-4878-94a6-0a6a9b56847b" />

*Figure 1: Installation and execution of basic programs.*

### 8.2 Synchronization Mechanisms Execution

<img width="791" height="716" alt="02_Synchronization_Mechanisms_Complete_Execution" src="https://github.com/user-attachments/assets/f01b6d11-78f8-40e9-bab9-cf6468586704" />

*Figure 2: Execution of synchronization mechanism programs.*

### 8.3 Synchronization Comparison Results

<img width="713" height="491" alt="03_Synchronization_Comparison_Results" src="https://github.com/user-attachments/assets/8860555c-60ac-451b-9062-61dc176330f1" />

*Figure 3: Execution results comparing different synchronization mechanisms.*

## 9. Sample Output of the Comparison Program

A representative run is shown below. The execution times and results may vary depending on the machine, virtual machine configuration, and number of CPU cores.

```text
Comparing synchronization mechanisms for 10000000 shared increments

Mechanism | Threads | Final Count | Correctness | Time (s)
---------------------------------------------------------------
None      | 1       | 10000000   | Correct     | 0.0486
Critical  | 1       | 10000000   | Correct     | 0.1571
Atomic    | 1       | 10000000   | Correct     | 0.0567
Lock      | 1       | 10000000   | Correct     | 0.1586
---------------------------------------------------------------
None      | 2       | 10000000   | Correct     | 0.0249
Critical  | 2       | 10000000   | Correct     | 0.1584
Atomic    | 2       | 10000000   | Correct     | 0.0574
Lock      | 2       | 10000000   | Correct     | 0.1590
---------------------------------------------------------------
None      | 4       | 7545062    | INCORRECT   | 0.0250
Critical  | 4       | 10000000   | Correct     | 0.1583
Atomic    | 4       | 10000000   | Correct     | 0.0585
Lock      | 4       | 10000000   | Correct     | 0.1615
---------------------------------------------------------------
None      | 8       | 4394535    | INCORRECT   | 0.0250
Critical  | 8       | 10000000   | Correct     | 0.1579
Atomic    | 8       | 10000000   | Correct     | 0.0565
Lock      | 8       | 10000000   | Correct     | 0.1603
---------------------------------------------------------------

Expected correct final count = 10000000

Observation: 'None' is fastest but incorrect (race condition).
'Critical' is correct but slowest (coarse-grained locking).
'Atomic' and 'Lock' are correct; 'Atomic' scales better since it
uses lightweight hardware instructions instead of OS-level locks.
```

### 9.1 Execution Time vs Number of Threads

<img width="923" height="546" alt="synchronization_execution_time" src="https://github.com/user-attachments/assets/d42cfce0-5327-435e-b3e8-d41d3f99c088" />

*Figure 4: Comparison of execution time for different synchronization mechanisms across 1, 2, 4, and 8 threads.*

### 9.2 Final Counter Value vs Number of Threads

<img width="920" height="548" alt="synchronization_final_counter" src="https://github.com/user-attachments/assets/965adc3d-fcdd-43b2-b675-13ce626036d2" />

*Figure 5: Comparison of final counter values for different synchronization mechanisms. The expected counter value is 10,000,000.*

### 9.3 Execution Time of Synchronization Methods

<img width="922" height="548" alt="synchronization_methods_time" src="https://github.com/user-attachments/assets/ca7400d9-07ec-4419-8125-cfce2c2b1343" />

*Figure 6: Comparison of execution time for Critical, Atomic, and Lock synchronization methods across 1, 2, 4, and 8 threads.*

### 9.4 Counter Correctness vs Number of Threads

<img width="923" height="547" alt="synchronization_correctness" src="https://github.com/user-attachments/assets/620c2027-efa6-46d2-9cb7-15e7cba34497" />

*Figure 7: Comparison of counter correctness percentage for different synchronization methods across 1, 2, 4, and 8 threads.*

## 10. Observation / Comparison Table

| Mechanism | Correctness | Relative Performance | Scalability |
|---|---|---|---|
| None (race condition) | Incorrect with multiple threads | Fastest (no synchronization overhead) | Poor – incorrect results can occur as thread count increases |
| Critical section | Correct | Slow due to serialized access | Poor to moderate – contention increases with thread count |
| Atomic operation | Correct | Fast for simple shared-variable updates | Good for simple operations |
| Lock (`omp_lock_t`) | Correct | Slower due to lock-management overhead | Poor to moderate |
| Barrier | Synchronizes execution phases | Introduces waiting overhead | Depends on how quickly threads reach the barrier |
| Semaphore | Correct when used properly | Moderate due to synchronization overhead | Moderate |

## 11. Conclusion

This experiment demonstrated the importance of synchronization mechanisms in multithreaded programming. The unsynchronized program was faster but produced incorrect results when multiple threads updated the shared counter, demonstrating a race condition.

Critical sections, atomic operations, locks, and semaphores helped ensure correct access to shared resources. Among the mechanisms tested, atomic operations provided a good balance of correctness and performance for simple shared-variable updates. Critical sections and locks introduced additional overhead because threads had to wait to access the protected region.

The barrier mechanism synchronized threads at specific execution points but did not directly protect shared data. Semaphores provided controlled access to shared resources. Overall, the experiment demonstrated that selecting an appropriate synchronization mechanism is essential for maintaining correctness and understanding the performance and scalability of multithreaded programs.

## 12. Project Directory Structure

```
Synchronization-Mechanisms
│
├── .gitignore
├── README.md
│
├── src/
│   ├── race.c
│   ├── critical.c
│   ├── atomic.c
│   ├── barrier.c
│   ├── semaphore.c
│   └── compare_sync.c
│
├── scripts/
│   ├── benchmark_visualizer.py
│   └── pgc_automation.sh
│
└── results/
    ├── figures/
    │   ├── synchronization_correctness.png
    │   ├── synchronization_execution_time.png
    │   ├── synchronization_final_counter.png
    │   └── synchronization_methods_time.png
    │
    └── images/
        ├── 01_Installation_and_Basic_Programs.png
        ├── 02_Synchronization_Mechanisms_Complete_Execution.png
        └── 03_Synchronization_Comparison_Results.png
```

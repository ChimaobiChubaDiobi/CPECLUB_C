#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 200

struct sinfo {
    char fname[50];
    char lname[50];
    int roll;
    float cgpa;
    int cid[5];
};

struct sinfo students[MAX_STUDENTS];
int count = 0;

/*Utility*/

void clearInput() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void printHeader() {
    printf("\n\n");
    printf("     STUDENT INFORMATION MANAGEMENT SYSTEM\n");
    printf("\n");
}

void printStudent(struct sinfo *s) {
    printf("  Name     : %s %s\n", s->fname, s->lname);
    printf("  Roll No  : %d\n", s->roll);
    printf("  CGPA     : %.2f\n", s->cgpa);
    printf("  Courses  : %d %d %d %d %d\n",
           s->cid[0], s->cid[1], s->cid[2], s->cid[3], s->cid[4]);
    printf("  ──────────────────────────────────────────────\n");
}

int findByRoll(int roll) {
    for (int i = 0; i < count; i++)
        if (students[i].roll == roll) return i;
    return -1;
}

/* ─── 1. Add Student Manually ─────────────────────────────── */

void addStudent() {
    if (count >= MAX_STUDENTS) {
        printf("[!] Database is full (%d records max).\n", MAX_STUDENTS);
        return;
    }

    struct sinfo s;

    printf("\n--- Add New Student ---\n");
    printf("First Name : "); scanf("%49s", s.fname);
    printf("Last Name  : "); scanf("%49s", s.lname);
    printf("Roll No    : "); scanf("%d", &s.roll);

    if (findByRoll(s.roll) != -1) {
        printf("[!] A student with Roll No %d already exists.\n", s.roll);
        return;
    }

    printf("CGPA       : "); scanf("%f", &s.cgpa);
    printf("Course IDs (5 values, space-separated): ");
    for (int i = 0; i < 5; i++) scanf("%d", &s.cid[i]);

    students[count++] = s;
    printf("[✓] Student '%s %s' added successfully.\n", s.fname, s.lname);
}

/* ─── 2. Bulk Import from TXT ─────────────────────────────── */

void bulkImport() {
    char filename[100];
    printf("\nEnter filename to import [default: students.txt]: ");
    clearInput();
    fgets(filename, sizeof(filename), stdin);
    filename[strcspn(filename, "\n")] = '\0';
    if (strlen(filename) == 0) strcpy(filename, "students.txt");

    FILE *fp = fopen(filename, "r");
    if (!fp) {
        printf("[!] Cannot open '%s'. Check the file exists in the same directory.\n", filename);
        return;
    }

    int imported = 0, skipped = 0;
    struct sinfo s;

    while (fscanf(fp, "%49s %49s %d %f %d %d %d %d %d",
                  s.fname, s.lname, &s.roll, &s.cgpa,
                  &s.cid[0], &s.cid[1], &s.cid[2], &s.cid[3], &s.cid[4]) == 9) {

        if (count >= MAX_STUDENTS) {
            printf("[!] Max capacity reached. Remaining records skipped.\n");
            break;
        }
        if (findByRoll(s.roll) != -1) {
            printf("[~] Skipping duplicate Roll No %d (%s %s).\n", s.roll, s.fname, s.lname);
            skipped++;
            continue;
        }
        students[count++] = s;
        imported++;
    }

    fclose(fp);
    printf("[✓] Import complete — %d added, %d skipped (duplicates).\n", imported, skipped);
}

/* ─── 3. Download / Export to TXT ────────────────────────── */

void downloadAll() {
    if (count == 0) {
        printf("[!] No records in memory to export.\n");
        return;
    }

    FILE *fp = fopen("database_backup.txt", "w");
    if (!fp) {
        printf("[!] Could not create 'database_backup.txt'.\n");
        return;
    }

    for (int i = 0; i < count; i++) {
        struct sinfo *s = &students[i];
        fprintf(fp, "%s %s %d %.2f %d %d %d %d %d\n",
                s->fname, s->lname, s->roll, s->cgpa,
                s->cid[0], s->cid[1], s->cid[2], s->cid[3], s->cid[4]);
    }

    fclose(fp);
    printf("[✓] %d record(s) exported to 'database_backup.txt'.\n", count);
}

/* ─── 4. Find by Roll Number ──────────────────────────────── */

void findByRollNo() {
    int roll;
    printf("\nEnter Roll Number to search: ");
    scanf("%d", &roll);

    int idx = findByRoll(roll);
    if (idx == -1) {
        printf("[!] No student found with Roll No %d.\n", roll);
    } else {
        printf("\n[✓] Student Found:\n");
        printStudent(&students[idx]);
    }
}

/* ─── 5. Find by First Name ───────────────────────────────── */

void findByFirstName() {
    char name[50];
    printf("\nEnter First Name to search: ");
    scanf("%49s", name);

    int found = 0;
    for (int i = 0; i < count; i++) {
        if (strcasecmp(students[i].fname, name) == 0) {
            if (!found) printf("\n[✓] Match(es) Found:\n");
            printStudent(&students[i]);
            found++;
        }
    }
    if (!found)
        printf("[!] No student found with first name '%s'.\n", name);
}

/* ─── 6. Delete by Roll Number ────────────────────────────── */

void deleteByRoll() {
    int roll;
    printf("\nEnter Roll Number to delete: ");
    scanf("%d", &roll);

    int idx = findByRoll(roll);
    if (idx == -1) {
        printf("[!] No student found with Roll No %d.\n", roll);
        return;
    }

    printf("  About to delete: %s %s (Roll: %d)\n",
           students[idx].fname, students[idx].lname, roll);
    printf("  Confirm? (y/n): ");
    char c; scanf(" %c", &c);
    if (c != 'y' && c != 'Y') {
        printf("[~] Deletion cancelled.\n");
        return;
    }

    /* Shift records left to fill the gap */
    for (int i = idx; i < count - 1; i++)
        students[i] = students[i + 1];
    count--;
    printf("[✓] Student with Roll No %d deleted.\n", roll);
}

/* ─── 7. Update by Roll Number ────────────────────────────── */

void updateByRoll() {
    int roll;
    printf("\nEnter Roll Number to update: ");
    scanf("%d", &roll);

    int idx = findByRoll(roll);
    if (idx == -1) {
        printf("[!] No student found with Roll No %d.\n", roll);
        return;
    }

    struct sinfo *s = &students[idx];
    printf("\n  Current Record:\n");
    printStudent(s);

    printf("  What would you like to update?\n");
    printf("  [1] First Name\n");
    printf("  [2] Last Name\n");
    printf("  [3] CGPA\n");
    printf("  [4] Course IDs\n");
    printf("  [5] All Fields\n");
    printf("  Choice: ");

    int choice; scanf("%d", &choice);

    switch (choice) {
        case 1:
            printf("  New First Name: "); scanf("%49s", s->fname);
            break;
        case 2:
            printf("  New Last Name : "); scanf("%49s", s->lname);
            break;
        case 3:
            printf("  New CGPA      : "); scanf("%f", &s->cgpa);
            break;
        case 4:
            printf("  New Course IDs (5 values): ");
            for (int i = 0; i < 5; i++) scanf("%d", &s->cid[i]);
            break;
        case 5:
            printf("  First Name    : "); scanf("%49s", s->fname);
            printf("  Last Name     : "); scanf("%49s", s->lname);
            printf("  CGPA          : "); scanf("%f", &s->cgpa);
            printf("  Course IDs (5): ");
            for (int i = 0; i < 5; i++) scanf("%d", &s->cid[i]);
            break;
        default:
            printf("[!] Invalid choice. Update cancelled.\n");
            return;
    }

    printf("[✓] Record updated successfully.\n");
    printStudent(s);
}

/* ─── Menu ────────────────────────────────────────────────── */

void showMenu() {
    printf("\n  ┌─────────────────────────────────────┐\n");
    printf("  │           MAIN MENU                 │\n");
    printf("  ├─────────────────────────────────────┤\n");
    printf("  │  1. Add Student (Manual)            │\n");
    printf("  │  2. Bulk Import from .txt           │\n");
    printf("  │  3. Download All to .txt            │\n");
    printf("  │  4. Find by Roll Number             │\n");
    printf("  │  5. Find by First Name              │\n");
    printf("  │  6. Delete by Roll Number           │\n");
    printf("  │  7. Update by Roll Number           │\n");
    printf("  │  8. Exit                            │\n");
    printf("  └─────────────────────────────────────┘\n");
    printf("  Records in memory: %d\n", count);
    printf("  Choice: ");
}

/* ─── Main ────────────────────────────────────────────────── */

int main() {
    int choice;

    printHeader();

    do {
        showMenu();
        if (scanf("%d", &choice) != 1) {
            clearInput();
            printf("[!] Invalid input. Please enter a number.\n");
            continue;
        }

        switch (choice) {
            case 1: addStudent();      break;
            case 2: bulkImport();      break;
            case 3: downloadAll();     break;
            case 4: findByRollNo();    break;
            case 5: findByFirstName(); break;
            case 6: deleteByRoll();    break;
            case 7: updateByRoll();    break;
            case 8: printf("\n[✓] Exiting. Goodbye!\n\n"); break;
            default: printf("[!] Invalid option. Choose 1–8.\n");
        }

    } while (choice != 8);

    return 0;
}
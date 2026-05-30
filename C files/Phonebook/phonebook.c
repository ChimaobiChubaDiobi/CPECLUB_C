#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LEN 50
#define MAX_PHONE_LEN 15
#define MAX_CONTACTS 100

// Contact structure with fixed-size character arrays
typedef struct {
    char name[MAX_NAME_LEN];
    char phone[MAX_PHONE_LEN];
} Contact;

// Phonebook structure
typedef struct {
    Contact contacts[MAX_CONTACTS];
    int count;
} Phonebook;

// Function prototypes - all use pointers to demonstrate memory address manipulation
void init_phonebook(Phonebook *pb);
int add_contact(Phonebook *pb, const char *name, const char *phone);
int search_contact(Phonebook *pb, const char *name);
int delete_contact(Phonebook *pb, const char *name);
void list_all_contacts(Phonebook *pb);
int update_contact(Phonebook *pb, const char *name, const char *new_name, const char *new_phone);
void display_menu();
void clear_input_buffer();

int main() {
    Phonebook phonebook;
    int choice;
    char name[MAX_NAME_LEN];
    char phone[MAX_PHONE_LEN];
    char new_name[MAX_NAME_LEN];
    char new_phone[MAX_PHONE_LEN];
    
    // Initialize phonebook (passing pointer to the struct)
    init_phonebook(&phonebook);
    
    while (1) {
        display_menu();
        printf("Enter your choice: ");
        scanf("%d", &choice);
        clear_input_buffer();
        
        switch (choice) {
            case 1: // Add contact
                printf("Enter name: ");
                fgets(name, MAX_NAME_LEN, stdin);
                name[strcspn(name, "\n")] = '\0'; // Remove newline
                
                if (strlen(name) == 0) {
                    printf("Name cannot be empty!\n");
                    break;
                }
                
                printf("Enter phone number: ");
                fgets(phone, MAX_PHONE_LEN, stdin);
                phone[strcspn(phone, "\n")] = '\0';
                
                if (add_contact(&phonebook, name, phone)) {
                    printf("Contact added successfully!\n");
                } else {
                    printf("Failed to add contact (phonebook may be full).\n");
                }
                break;
                
            case 2: // Search contact
                printf("Enter name to search: ");
                fgets(name, MAX_NAME_LEN, stdin);
                name[strcspn(name, "\n")] = '\0';
                search_contact(&phonebook, name);
                break;
                
            case 3: // Delete contact
                printf("Enter name to delete: ");
                fgets(name, MAX_NAME_LEN, stdin);
                name[strcspn(name, "\n")] = '\0';
                if (delete_contact(&phonebook, name)) {
                    printf("Contact deleted successfully!\n");
                }
                break;
                
            case 4: // List all contacts
                list_all_contacts(&phonebook);
                break;
                
            case 5: // Update contact
                printf("Enter current name: ");
                fgets(name, MAX_NAME_LEN, stdin);
                name[strcspn(name, "\n")] = '\0';
                
                printf("Enter new name (press Enter to keep): ");
                fgets(new_name, MAX_NAME_LEN, stdin);
                new_name[strcspn(new_name, "\n")] = '\0';
                
                printf("Enter new phone (press Enter to keep): ");
                fgets(new_phone, MAX_PHONE_LEN, stdin);
                new_phone[strcspn(new_phone, "\n")] = '\0';
                
                if (update_contact(&phonebook, name, new_name, new_phone)) {
                    printf("Contact updated successfully!\n");
                }
                break;
                
            case 0: // Exit
                printf("Exiting Phonebook. Goodbye!\n");
                return 0;
                
            default:
                printf("Invalid choice! Please try again.\n");
        }
    }
    
    return 0;
}

// Initialize phonebook (sets count to 0)
void init_phonebook(Phonebook *pb) {
    pb->count = 0;
    printf("Phonebook initialized. Memory address: %p\n", (void*)pb);
}

// Add a new contact using pointer to phonebook
int add_contact(Phonebook *pb, const char *name, const char *phone) {
    // Check if phonebook is full
    if (pb->count >= MAX_CONTACTS) {
        return 0;
    }
    
    // Get pointer to the new contact's memory location
    Contact *new_contact = &(pb->contacts[pb->count]);
    
    // Demonstrate pointer concept: new_contact stores a memory address
    printf("[DEBUG] Storing contact at memory address: %p\n", (void*)new_contact);
    printf("[DEBUG] Name will be stored at: %p\n", (void*)new_contact->name);
    printf("[DEBUG] Phone will be stored at: %p\n", (void*)new_contact->phone);
    
    // Copy strings (ensuring null termination)
    strncpy(new_contact->name, name, MAX_NAME_LEN - 1);
    new_contact->name[MAX_NAME_LEN - 1] = '\0';
    
    strncpy(new_contact->phone, phone, MAX_PHONE_LEN - 1);
    new_contact->phone[MAX_PHONE_LEN - 1] = '\0';
    
    pb->count++;
    return 1;
}

// Search for contacts (case-insensitive)
int search_contact(Phonebook *pb, const char *name) {
    int found = 0;
    printf("\n=== Search Results ===\n");
    
    for (int i = 0; i < pb->count; i++) {
        // Get pointer to current contact
        Contact *current = &(pb->contacts[i]);
        
        // Case-insensitive search using strcasestr (or strstr on Windows)
        if (strstr(current->name, name) != NULL) {
            printf("Contact %d: %s -> %s\n", i + 1, current->name, current->phone);
            found = 1;
        }
    }
    
    if (!found) {
        printf("No contact found with name containing '%s'\n", name);
    }
    printf("\n");
    return found;
}

// Delete a contact by name
int delete_contact(Phonebook *pb, const char *name) {
    for (int i = 0; i < pb->count; i++) {
        Contact *current = &(pb->contacts[i]);
        
        if (strcasecmp(current->name, name) == 0) {
            printf("[DEBUG] Deleting contact at memory address: %p\n", (void*)current);
            
            // Shift all subsequent contacts left
            for (int j = i; j < pb->count - 1; j++) {
                pb->contacts[j] = pb->contacts[j + 1];
            }
            pb->count--;
            return 1;
        }
    }
    
    printf("Contact '%s' not found.\n", name);
    return 0;
}

// List all contacts in phonebook
void list_all_contacts(Phonebook *pb) {
    if (pb->count == 0) {
        printf("\nPhonebook is empty.\n");
        return;
    }
    
    printf("\n=== Phonebook Contacts ===\n");
    printf("%-4s %-30s %-15s\n", "No.", "Name", "Phone");
    printf("--------------------------------------------------\n");
    
    for (int i = 0; i < pb->count; i++) {
        Contact *current = &(pb->contacts[i]);
        printf("%-4d %-30s %-15s\n", i + 1, current->name, current->phone);
    }
    printf("Total: %d contacts\n\n", pb->count);
}

// Update contact information
int update_contact(Phonebook *pb, const char *name, const char *new_name, const char *new_phone) {
    for (int i = 0; i < pb->count; i++) {
        Contact *current = &(pb->contacts[i]);
        
        if (strcasecmp(current->name, name) == 0) {
            printf("[DEBUG] Updating contact at memory address: %p\n", (void*)current);
            
            // Update name if provided
            if (strlen(new_name) > 0) {
                printf("[DEBUG] Updating name at address: %p\n", (void*)current->name);
                strncpy(current->name, new_name, MAX_NAME_LEN - 1);
                current->name[MAX_NAME_LEN - 1] = '\0';
            }
            
            // Update phone if provided
            if (strlen(new_phone) > 0) {
                printf("[DEBUG] Updating phone at address: %p\n", (void*)current->phone);
                strncpy(current->phone, new_phone, MAX_PHONE_LEN - 1);
                current->phone[MAX_PHONE_LEN - 1] = '\0';
            }
            
            return 1;
        }
    }
    
    printf("Contact '%s' not found.\n", name);
    return 0;
}

// Display menu options
void display_menu() {
    printf("\n==================================================\n");
    printf("        PHONEBOOK MANAGEMENT SYSTEM\n");
    printf("==================================================\n");
    printf("1. Add Contact\n");
    printf("2. Search Contact\n");
    printf("3. Delete Contact\n");
    printf("4. List All Contacts\n");
    printf("5. Update Contact\n");
    printf("0. Exit\n");
    printf("--------------------------------------------------\n");
}

// Clear input buffer
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}
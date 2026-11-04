// concurrent Linked List design
// LinkedList allows folloing operation:
// static: 
//      get_at(i) set_at(i,key)           || O(n) O(n)
// dynamic: 
//      insert_first() insert_last()      || O(1) O(n)
//      delete_first() delete_last()      || O(1) O(n)
//      insert_at(i, key) delete_at(i)    || O(n) O(n)
// 
// Concurrent techniques on linked list:
// 1. Coarse-Grained Synchronization
// 2. Fine-Grained Synchronization
// 3. Optimistic Synchronization
// 4. lazy synchronization
// 5. Non-blocking synchronization

#include "LinkedListNode.h"
#include <vector>

class UnSyncLinkedList{
    public:
        UnSyncLinkedList() = default;
        UnSyncLinkedList(const std::vector<int>& arr);
        
        ~UnSyncLinkedList(){
            LinkedListNode *curr, *freed;
            
              curr = m_head;
              while (curr != nullptr) {
                freed = curr;
                curr = curr->next;
                delete freed;
              }
        };
        // derived class have to override these methods
        virtual void add(int key) = 0 ;
        virtual bool remove(int key) = 0 ; // return -1 if not found
        virtual int getSize()  = 0;
        virtual void display()  = 0;

        void m_display();
    protected:
        void m_add(int key);
        bool m_remove(int key);
        int m_getSize();
        LinkedListNode* m_head{nullptr};
        LinkedListNode* m_tail{nullptr};

    private:
        int m_size{0};
};
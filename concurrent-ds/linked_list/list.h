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




// Coarse-Grained Synchronization:
// take a sequential implementation of the class, add a scalable lock field, and ensure
// that each method call acquires and releases that lock. We call this approach
// coarse-grained synchronization.

class LinkedListNode{
    public:
        // node constructor
        explicit LinkedListNode(int key);
        ~LinkedListNode() = default;
        // node specific method
        LinkedListNode* laterNode(int idx);
        
        int key;
        LinkedListNode* next{nullptr};
        
};


class UnSyncLinkedList{
    public:
        virtual void add();
};

#include <mutex>
class CoraseGrainedLinkedList{
    private:
        std::mutex mut_;

    public:
};
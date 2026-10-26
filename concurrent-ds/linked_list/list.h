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
#include <vector>
class LinkedList{
    public: 
        LinkedList();
        LinkedList(int len);
        LinkedList(std::vector<int> arr);
        
};
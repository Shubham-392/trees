// fine-grained linked list with it's own 
// linkedlist node having lock per node
// 
#include <mutex>
class FineGrainNode{
    public:
        FineGrainNode(int key);
        FineGrainNode(int key, FineGrainNode* next );
        FineGrainNode(const FineGrainNode& node);
        int m_key;
        FineGrainNode* m_next{nullptr};
        std::mutex mux_;
};


class FineGrainLinkedList{
    // sentinel nodes are allowed
    private:
        FineGrainNode* m_head{nullptr};
        FineGrainNode* m_tail{nullptr};
    public:
        // constructor and destructor
        FineGrainLinkedList();
        ~FineGrainLinkedList();
        
        bool add(int item);
        bool remove(int item);
        bool contains(int item);
};
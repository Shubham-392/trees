class LinkedListNode{
    public:
        // node constructor
        explicit LinkedListNode(int key);
        explicit LinkedListNode(int key, LinkedListNode* next );
        explicit LinkedListNode(const LinkedListNode& node);
        
        ~LinkedListNode() = default;
        
        int key;
        LinkedListNode* next{nullptr};
        
};
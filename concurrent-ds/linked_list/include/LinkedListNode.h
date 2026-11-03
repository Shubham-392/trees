class LinkedListNode{
    public:
        // node constructor
        LinkedListNode(int key);
        LinkedListNode(int key, LinkedListNode* next );
        LinkedListNode(const LinkedListNode& node);
        
        ~LinkedListNode() = default;
        
        int key;
        LinkedListNode* next{nullptr};
        
};
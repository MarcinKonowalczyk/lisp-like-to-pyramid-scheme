from itertools import zip_longest, tee
from math import ceil,sqrt

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class Tree:
    '''
    Tree of pyramids
    '''

    @staticmethod
    def text_to_grid(text,min_len=0,space='.',remove_spaces=True):
        '''
        Put text in a pyramid
        '''
        # N = ceil(sqrt(len(text))) # Number of pyramid levels
        s = space
        if remove_spaces: text = text.replace(' ','')

        # Ensure nice formatting of short keywords (without excessive space)
        if len(text)==2: text = space + text
        elif len(text)==3: text = space + text
        elif len(text)==5: text = 4*space + text
        elif len(text)==6: text = space + text[:3] + space + text[3:]
        elif len(text)==7: text = text[:4] + space + text[4:]
        elif len(text)==10: text = 4*space + text[:5] + space + text[5:]

        level = 0
        lines = ['^']
        while text:
            level += 1
            i = 2*level-1
            front, text = (text[:i],text[i:])
            pad = i-len(front)
            lines.append('/' + front + pad*s + '\\')
        lines.append('-'*(2*level+1))
        grid = [(level-j+1,line,level-j+1) for j,line in enumerate(lines)]
        grid[-1] = (1,grid[-1][1],1) # Correct the padding of the final row
        return grid

    @staticmethod
    def grid2string(grid,space='.'):
        return '\n'.join([space*l + row + space*r for l,row,r in grid])

    @staticmethod
    def string2grid(string,space='.'):
        grid = []
        for row in string.split('\n'):
            i1,i2 = (0,len(row)+1)
            for i,(l1,l2) in enumerate(pairwise(row)):
                if l1==space and l2!=space and not i1: i1 = i+1
                if l1!=space and l2==space: i2 = i+1
            grid.append((i1,row[i1:i2],len(row)-i2))
        return grid

    def __init__(self,grid):
        self.height = len(grid)
        rowlen = lambda r: r[0] + len(r[1]) + r[2]
        self.width = rowlen(grid[0])
        for row in grid:
            assert isinstance(row,tuple), 'All rows of the grid must be tuples'
            assert len(row)==3, 'All rows must be 3-length tuples'
            assert rowlen(row)==self.width, 'All rows must specify entries of the same length'
        
        self.space = '.'
        self.grid = grid
        
    @classmethod
    def from_text(self,text):
        return self(self.text_to_grid(text))

    def __repr__(self):
        return f'<Grid #{hash(self)}:\n' + self.grid2string(self.grid) + '\n>'

    @staticmethod
    def row_iterator(left,right):
        for l,r in zip(left,right):
            # TODO: Add more detailed checking (making sure pyramids don't interfere)
            yield l[2]+r[0]-1

    def add_pyramid(self,other,tight=True,min_width=None):
        s = self.space

        # Find tightest squeeze between the pyramids
        squeeze = 0
        if tight:
            squeeze = min(self.row_iterator(self.grid,other.grid))
        
        # Decrease the squeeze if required by the min_width
        if min_width:
            r,l = self.grid[0],other.grid[0]
            closest_width = r[2]+l[0]-squeeze
            squeeze -= max(min_width-closest_width,0)

        squeezed_width = self.width+other.width-squeeze # Width of the squeezed pyramid
        # width = max(squeezed_width,self.width,other.width) # Actual width of the pyramid
        overhang = max(self.width,other.width)-squeezed_width # Signed overhang of one pyramid over the other
        lp,rp = (max(overhang,0),0)
        if self.height>other.height: lp,rp = rp,lp

        grid = []
        for l,r in zip_longest(self.grid,other.grid):
            if l and r:
                left_pad = lp + l[0]
                middle = l[1] + (l[2]+r[0]-squeeze)*s + r[1]
                right_pad = r[2] + rp
            elif l:
                left_pad = l[0]
                middle = l[1]
                right_pad = l[2]+max(0,-overhang)
            elif r:
                left_pad = max(0,-overhang)+r[0]
                middle = r[1]
                right_pad = r[2]
            row = (left_pad,middle,right_pad)
            grid.append(row)
        return Tree(grid)

if __name__ == '__main__':
    # p1 = Tree.from_keyword('Quick brown fox jumped over a lazy god'*10)
    # p1 = Tree.from_keyword('Quick brown fox jumped over a lazy god')
    p1 = Tree.from_text('hello')
    p2 = Tree.from_text('Greetings traveller! Where goes thee this fine morning?'*8)
    # p2 = Tree.from_text('Greetings traveller! Where goes thee this fine morning?')
    # p2 = Tree.from_keyword('hello')
    print(p1.add_pyramid(p2).add_pyramid(p1).add_pyramid(p1).add_pyramid(p1).add_pyramid(p2))
    # p3 = p1.add_pyramid(p2)
    # print(p3.add_pyramid(p1).add_pyramid(p1))
    # print(p1.middle,p1.grid[0][p1.middle])


    # print(Tree(''))
    # print(Tree('1'))
    # print(Tree('12'))
    # print(Tree('set'))
    # print(Tree('seto'))
    # print(Tree('hello'))
    # print(Tree('hellos'))
    # print(Tree('1234567'))
    # print(Tree.text_to_grid('12345678'))
    # print(Tree.text_to_grid('123456789'))
    # print(Tree.text_to_grid('0123456789'))
    # print(Tree.text_to_grid('Are you Arron Burr, Sir?'))
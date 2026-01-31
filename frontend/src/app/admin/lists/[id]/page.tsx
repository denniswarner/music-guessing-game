"use client";

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ArrowLeft, Save, Plus, Trash2, Music, Search } from 'lucide-react';
import { getList, updateList, deleteSong, createList, getCategories } from '@/lib/admin-api';
import type { CustomSongList, CategoryOptions, CustomSong } from '@/lib/admin-types';
import { SongSearch } from '@/components/admin/song-search';
import { toast } from 'sonner';

export default function ListEditorPage() {
  const router = useRouter();
  const params = useParams();
  const isNewList = params.id === 'new';
  
  const [list, setList] = useState<CustomSongList | null>(null);
  const [categories, setCategories] = useState<CategoryOptions | null>(null);
  const [isLoading, setIsLoading] = useState(!isNewList);
  const [isSaving, setIsSaving] = useState(false);
  const [showSongSearch, setShowSongSearch] = useState(false);
  
  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [targetAudience, setTargetAudience] = useState('');
  const [primaryDecade, setPrimaryDecade] = useState('');
  const [primaryGenre, setPrimaryGenre] = useState('');

  useEffect(() => {
    loadCategories();
    if (!isNewList) {
      loadList();
    }
  }, [params.id]);

  const loadCategories = async () => {
    try {
      const cats = await getCategories();
      setCategories(cats);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const loadList = async () => {
    try {
      setIsLoading(true);
      const data = await getList(params.id as string);
      setList(data);
      setName(data.name);
      setDescription(data.description || '');
      setTargetAudience(data.target_audience || '');
      setPrimaryDecade(data.primary_decade || '');
      setPrimaryGenre(data.primary_genre || '');
    } catch (err: any) {
      console.error('Failed to load list:', err);
      alert('Failed to load list');
      router.push('/admin');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!name.trim()) {
      toast.error('List name is required');
      return;
    }

    try {
      setIsSaving(true);
      
      if (isNewList) {
        const newList = await createList({
          name: name.trim(),
          description: description.trim() || undefined,
          target_audience: targetAudience.trim() || undefined,
          primary_decade: primaryDecade || undefined,
          primary_genre: primaryGenre || undefined,
        });
        toast.success('Playlist created successfully!', {
          description: `"${newList.name}" has been created.`
        });
        router.push(`/admin/lists/${newList.id}`);
      } else {
        await updateList(params.id as string, {
          name: name.trim(),
          description: description.trim() || undefined,
          target_audience: targetAudience.trim() || undefined,
          primary_decade: primaryDecade || undefined,
          primary_genre: primaryGenre || undefined,
        });
        await loadList();
        toast.success('Playlist saved successfully!', {
          description: `"${name.trim()}" has been updated.`
        });
      }
    } catch (err: any) {
      console.error('Failed to save list:', err);
      toast.error('Failed to save playlist', {
        description: err.message || 'An error occurred while saving.'
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleRemoveSong = async (songId: string) => {
    if (!confirm('Remove this song from the list?')) return;
    
    try {
      await deleteSong(params.id as string, songId);
      await loadList();
      toast.success('Song removed from playlist');
    } catch (err) {
      console.error('Failed to remove song:', err);
      toast.error('Failed to remove song');
    }
  };

  const handleSongAdded = () => {
    setShowSongSearch(false);
    loadList();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.push('/admin')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <h1 className="text-3xl font-bold">
              {isNewList ? 'Create New List' : 'Edit List'}
            </h1>
          </div>
          <Button onClick={handleSave} disabled={isSaving} className="gap-2">
            <Save className="h-4 w-4" />
            {isSaving ? 'Saving...' : 'Save'}
          </Button>
        </div>

        {/* List Details */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>List Details</CardTitle>
            <CardDescription>
              Basic information about your custom song list
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">List Name *</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g., 80s Rock Classics"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the list and its purpose..."
                rows={3}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="target">Target Audience</Label>
                <Input
                  id="target"
                  value={targetAudience}
                  onChange={(e) => setTargetAudience(e.target.value)}
                  placeholder="e.g., Corporate Event"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="decade">Primary Decade</Label>
                <Select value={primaryDecade || "none"} onValueChange={(v) => setPrimaryDecade(v === "none" ? "" : v)}>
                  <SelectTrigger id="decade">
                    <SelectValue placeholder="Select decade" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">None</SelectItem>
                    {categories?.decades.map((d) => (
                      <SelectItem key={d} value={d}>{d}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="genre">Primary Genre</Label>
                <Select value={primaryGenre || "none"} onValueChange={(v) => setPrimaryGenre(v === "none" ? "" : v)}>
                  <SelectTrigger id="genre">
                    <SelectValue placeholder="Select genre" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">None</SelectItem>
                    {categories?.genres.map((g) => (
                      <SelectItem key={g} value={g}>{g}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Songs Section */}
        {!isNewList && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Songs ({list?.songs.length || 0})</CardTitle>
                  <CardDescription>
                    Manage songs in this list
                  </CardDescription>
                </div>
                <Button onClick={() => setShowSongSearch(true)} className="gap-2">
                  <Plus className="h-4 w-4" />
                  Add Songs
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {!list?.songs.length ? (
                <div className="text-center py-8">
                  <Music className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-muted-foreground mb-4">No songs yet</p>
                  <Button onClick={() => setShowSongSearch(true)} variant="outline" className="gap-2">
                    <Plus className="h-4 w-4" />
                    Add Your First Song
                  </Button>
                </div>
              ) : (
                <div className="space-y-3">
                  {list.songs.map((song) => (
                    <div
                      key={song.id}
                      className="flex items-start gap-3 p-3 rounded-lg border hover:bg-accent transition-colors"
                    >
                      <Music className="h-5 w-5 mt-1 text-muted-foreground flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium truncate">{song.name}</div>
                        <div className="text-sm text-muted-foreground truncate">
                          {song.artist}
                          {song.album && ` • ${song.album}`}
                        </div>
                        <div className="flex flex-wrap gap-1 mt-2">
                          {song.decade && (
                            <Badge variant="secondary" className="text-xs">{song.decade}</Badge>
                          )}
                          {song.genre && (
                            <Badge variant="secondary" className="text-xs">{song.genre}</Badge>
                          )}
                          {song.style && (
                            <Badge variant="outline" className="text-xs">{song.style}</Badge>
                          )}
                          {song.mood && (
                            <Badge variant="outline" className="text-xs">{song.mood}</Badge>
                          )}
                          {song.difficulty && (
                            <Badge variant="outline" className="text-xs capitalize">
                              {song.difficulty}
                            </Badge>
                          )}
                        </div>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleRemoveSong(song.id)}
                        className="flex-shrink-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Song Search Modal */}
        {showSongSearch && !isNewList && (
          <SongSearch
            listId={params.id as string}
            categories={categories}
            onClose={() => setShowSongSearch(false)}
            onSongAdded={handleSongAdded}
          />
        )}
      </div>
    </div>
  );
}
